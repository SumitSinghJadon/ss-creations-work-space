from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is require')

        user = self.model(username=username, **extra_fields)

        if extra_fields.get('is_superuser') :
            user.set_password(password)
        else:
            user.set_password(make_password(password))

        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('full_name', 'Super Admin')
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if not username:
            raise ValueError('Username is require')

        if not extra_fields.get('is_staff') :
            raise ValueError(('Super user must have is_staff True'))

        return self.create_user(username, password, **extra_fields)

