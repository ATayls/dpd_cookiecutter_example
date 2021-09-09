from django.urls import path
import dpd_cc_example.dashboard.views as views
from dpd_cc_example.dashboard.dash_app_scripts import basic_dash_app

app_name = "dashboard_test"
urlpatterns = [
    path('BasicApp', views.BasicDashApp, name='BasicDashApp'),
]
