from django.core.management.base import BaseCommand
from django.utils import timezone

from pathlib import Path

from dpd_cc_example.data.models import Team, PlayerResults

import pandas as pd

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

        self.csv_files_import()

    def csv_files_import(self):

        DATA_PATH = Path(__file__).resolve().parent.parent.parent.joinpath("example_raw_data")

        path_list = [p for p in DATA_PATH.glob('*')]

        teams_df = pd.read_csv(DATA_PATH.joinpath("teams.csv"))
        teams_df = teams_df.fillna(0.0)
        team_model_instances = [Team(**record) for record in teams_df.to_dict('records')]
        Team.objects.bulk_create(team_model_instances, ignore_conflicts=True)

        player_model_instances = []
        for p in DATA_PATH.glob('*'):
            df = pd.read_csv(p)
            if "gw" in p.stem:
                gw = int(p.stem.split("gw")[-1])
                match_subset = df[["team_a_score", "team_h_score", "kickoff_time", "was_home", "opponent_team"]].drop_duplicates().sort_values(by="opponent_team").copy()
                home_matches_only = match_subset[match_subset["was_home"] == True]
                away_matches_only = match_subset[match_subset["was_home"] == False]

                home_matches = home_matches_only.merge(away_matches_only, on=["team_h_score","team_a_score","kickoff_time"])
                away_matches = away_matches_only.merge(home_matches_only,on=["team_h_score", "team_a_score", "kickoff_time"])
                matches_all = pd.concat([home_matches, away_matches]).rename(
                    columns={"opponent_team_x":"opponent_team", "opponent_team_y":"team"}
                )

                df["id"] = df["element"].astype(str) + f"_{gw}"
                df["gw"] = gw
                df["name"] = df["name"].apply(lambda x: "_".join(x.split("_")[0:-1]))
                df["team"] = df["opponent_team"].apply(lambda x: matches_all[matches_all["opponent_team"]==x]["team"].values[0])
                df["was_home"] = df["was_home"].astype(int)
                df["team"] = df["team"].apply(lambda x: Team.objects.filter(id=x).first())
                df["opponent_team"] = df["opponent_team"].apply(lambda x: Team.objects.filter(id=x).first())
                df = df.dropna()
                df_records = df.to_dict('records')
                player_model_instances = [PlayerResults(**record) for record in df_records]

            self.stdout.write(f"Adding {len(df_records)} player results for gw{gw}")
            PlayerResults.objects.bulk_create(player_model_instances, ignore_conflicts=True)
