from django.urls import path
from dpd_cc_example.example.views import (
    BlogListView,
    BlogDetailView,
)

app_name = "example"

urlpatterns = [
    path("blog/<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
]
