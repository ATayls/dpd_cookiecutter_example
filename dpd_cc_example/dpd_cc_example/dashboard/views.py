from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def BasicDashApp(request):
    return render(request, 'pages/basic_dashboard.html')

def ReportApp(request):
    return render(request, 'pages/report_app.html')

