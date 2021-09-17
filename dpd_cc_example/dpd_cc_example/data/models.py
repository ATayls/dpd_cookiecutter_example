from django.db import models


class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.IntegerField()
    draw = models.IntegerField(default=0)
    form = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    name = models.TextField()
    played = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    position = models.IntegerField(default=0)
    pulse_id = models.IntegerField()
    short_name = models.TextField()
    strength = models.IntegerField(default=0)
    strength_attack_away = models.IntegerField(default=0)
    strength_attack_home = models.IntegerField(default=0)
    strength_defence_away = models.IntegerField(default=0)
    strength_defence_home = models.IntegerField(default=0)
    strength_overall_away = models.IntegerField(default=0)
    strength_overall_home = models.IntegerField(default=0)
    team_division = models.IntegerField(default=0)
    unavailable = models.IntegerField(default=0)
    win = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class PlayerResults(models.Model):
    id = models.TextField(primary_key=True)
    name=models.TextField()
    team=models.ForeignKey(Team, on_delete=models.CASCADE)
    gw=models.IntegerField()
    assists=models.IntegerField(default=0)
    bonus=models.IntegerField(default=0)
    bps=models.IntegerField(default=0)
    clean_sheets=models.IntegerField(default=0)
    creativity=models.FloatField(default=0)
    element=models.IntegerField()
    fixture=models.IntegerField()
    goals_conceded=models.IntegerField(default=0)
    goals_scored=models.IntegerField(default=0)
    ict_index=models.FloatField(default=0)
    influence=models.FloatField(default=0)
    kickoff_time=models.DateTimeField()
    minutes=models.IntegerField(default=0)
    opponent_team=models.ForeignKey(Team,  related_name='team_opponent', on_delete=models.CASCADE)
    own_goals=models.IntegerField(default=0)
    penalties_missed=models.IntegerField(default=0)
    penalties_saved=models.IntegerField(default=0)
    red_cards=models.IntegerField(default=0)
    round=models.IntegerField(default=0)
    saves=models.IntegerField(default=0)
    selected=models.IntegerField(default=0)
    team_a_score=models.IntegerField(default=0)
    team_h_score=models.IntegerField(default=0)
    threat=models.FloatField(default=0)
    total_points=models.IntegerField(default=0)
    transfers_balance=models.IntegerField(default=0)
    transfers_in=models.IntegerField(default=0)
    transfers_out=models.IntegerField(default=0)
    value=models.IntegerField(default=0)
    was_home=models.IntegerField(default=0)
    yellow_cards=models.IntegerField(default=0)

    def __str__(self):
        return self.name
