from django.shortcuts import render

def BasicDashApp(request):
    return render(request, 'pages/basic_dashboard.html')

