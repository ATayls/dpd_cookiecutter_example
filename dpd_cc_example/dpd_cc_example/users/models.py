import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import CharField, EmailField, BooleanField, DateTimeField, UUIDField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ An abstract base class implementing a custom user model + permissions"""
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = EmailField(
        max_length=254,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    name = CharField(_('Name'), max_length=254, null=True, blank=True)

    is_staff = BooleanField(
        _('Staff Status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_superuser = BooleanField(
        _('SuperUser Status'),
        default=False,
        help_text=_('Designates whether the user has all permissions.'),
    )

    is_active = BooleanField(
        _('Active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    # Audit Values
    # last_login = DateTimeField(
    #     _('Last Login'),
    #     default=timezone.now,
    # )
    date_joined = DateTimeField(
        _('Date Joined'),
        default=timezone.now
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [
        'name'
    ]

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
