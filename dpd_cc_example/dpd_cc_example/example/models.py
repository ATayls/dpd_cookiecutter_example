from django.db import models
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES = [
    ("draft", "Draft"),
    ("complete", "Published"),
]

class Post(models.Model):
    """ Model for example blog post """
    title = models.CharField(max_length=164)
    slug = models.SlugField(max_length=140, default=title)
    summary = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Post")

    def __str__(self):
        return self.title
