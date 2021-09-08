# dpd_cookiecutter_example
Example setup for django plotly dash with django cookiecutter

### Framework docs
- https://cookiecutter-django.readthedocs.io/en/latest/index.html
- https://django-plotly-dash.readthedocs.io/en/latest/index.html

### Useful tutorials
https://learnetto.com/users/vgreyes 
 - tutorial repo: https://github.com/reyesvicente/cookiecutter-blog-tutorial-learnetto

## Setup

### Cookiecutter setup

1. Create empty folder dpd_cookiecutter_example
2. Create venv
3. pip install cookiecutter
4. cookiecutter gh:pydanny/cookiecutter-django
5. cookiecutter defaults except
    - use_docker: y
    - cloud_provider: None
    - use_mailhog: y
    - use_whitenoise: y
6. cd dpd_cc_example

### Django plotly dash setup
1. Add dpd packages to requirements (problems with dash 2.0 and django plotly dash)
    - dash==1.21
    - django-plotly-dash==1.6.5
    - dpd-static-support (for bootstrap)
    - django-bootstrap4 (for bootstrap)
2. Update base settings for dpd:


    INSTALLED_APPS 
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'dpd_components',
    'dpd_static_support',
    'bootstrap4',
    
    MIDDLEWARE 
    'django_plotly_dash.middleware.BaseMiddleware',
    'django_plotly_dash.middleware.ExternalRedirectionMiddleware',

    X_FRAME_OPTIONS='SAMEORIGIN'
   
    STATICFILES_FINDERS
    "django_plotly_dash.finders.DashAssetFinder",
    "django_plotly_dash.finders.DashComponentFinder",
    "django_plotly_dash.finders.DashAppDirectoryFinder",
    
    PLOTLY_COMPONENTS=[
        'dash_core_components',
        'dash_html_components',
        'dash_renderer',
        'dpd_components'
    ]

### Build docker container

 At this stage, **if** developing locally the database should be created, environment variables set and
 local requirements should be pip installed. However docker compose is being used here these are **not necessary**.
    
    python -m pip install -r requirements/local.txt
    createdb dpd_example -U postgres --password <your_password>
    export DATABASE_URL=postgres://postgres:<enter_your_psql_password>@127.0.0.1:5432/dpd_example
    
2. Build and run the docker here to check everything is running as intended.
    - docker-compose -f local.yml build
    - docker-compose -f local.yml up
    - For other docker implementation details see https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html
    - Avoid this common error https://cookiecutter-django.readthedocs.io/en/latest/troubleshooting.html#docker-postgres-authentication-failed
3. While the container is running. Run these django management commands:
    - docker-compose -f local.yml run --rm django python manage.py makemigrations
    - docker-compose -f local.yml run --rm django python manage.py migrate
    - docker-compose -f local.yml run --rm django python manage.py createsuperuser
4. For pycharm debugging see:
    - https://testdriven.io/blog/django-debugging-pycharm/
    - https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html#run
    
## Create an example new App

see
 - https://github.com/pydanny/cookiecutter-django/issues/1725#issuecomment-407493176
 - https://github.com/pydanny/cookiecutter-django/issues/1876

1. python manage.py startapp <name-of-the-app> 
2. Move move <name-of-the-app> directory to <project_slug> directory
3. edit <project_slug>/<name-of-the-app>/apps.py
    - change name = "<name-of-the-app>" to name = "<project_slug>.<name-of-the-app>"
4. add "<project_slug>.<name-of-the-app>.apps.<NameOfTheAppConfigClass>" to LOCAL APPS in config/settings/base.py
    - optionally add verbose_name 
    - optionally modify ready method https://docs.djangoproject.com/en/3.2/ref/applications/
5. Create models views forms templates etc. In this repo:
    - Create a Post model
    - Create a List view and detail view (CBV) for the post model
    - Register Post model in admin.py
    - Create a template for the post view.
6. Add urls.py
    - app_name to match <name-of-the-app>
    - urlpatterns path("blog/\<slug:slug>/", BlogDetailView.as_view(), name="blog-detail")
7. Include app urls in config/urls.py
    - path("", include("dpd_cc_example.example.urls", namespace="example")),
8. Now we have edited the app. Run the container to test.
    - docker-compose -f local.yml build
    - docker-compose -f local.yml up
    - docker-compose -f local.yml run --rm django python manage.py makemigrations
    - docker-compose -f local.yml run --rm django python manage.py migrate
9. Create a new post in the admin page. Or use the shell to create a new post.
    - docker-compose -f local.yml run --rm django python manage.py shell
10. View post in http://0.0.0.0:8000/blog/<post-slug>
    
### Create a dash app

1. Ensure the django plotly dash setup has been complete.
2. Add django plotly dash to config/urls.py. Required for all dpd apps.
    -   path('django_plotly_dash/', include('django_plotly_dash.urls'))
3. Create the new django app with startapp. Follow steps 1-4 in example app section.
4. Create the pure plotly-dash app somewhere within your <name-of-the-app> folder. 
5. Replace the normal dash app registration with the DjangoDash class.
6. Create the template containing the dash app (https://django-plotly-dash.readthedocs.io/en/latest/template_tags.html):
    ```
    {%load plotly_dash%}
    {%plotly_app name="SimpleExample"%}
    ```
    
    or using plotly_class to apply class names to plotly app template. Use plotly_direct to remove app from within iframe:
    ```
    <div class="{% plotly_class name='<DjangoDash-app-name>' %} card" style="...">
        {% plotly_direct name='<DjangoDash-app-name>'  %}
    </div>
    ```
7. Create view to render the template.
8. Add urlpattern to app urls.py
    - path('<url-slug>', <view-object>, name='<name-of-dash-app>'),
    - here we also import the dash-app.py itself. (This can alternatively be done in views.py)
9. Include the urls in config/urls.py.
    - path('<define-url>/', include('<app-name>.urls')),
10. Optionally add a nav link to base template.