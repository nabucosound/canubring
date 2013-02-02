from django.contrib.auth.models import User


class UserAlreadyExists(Exception):
    """User that is being created already exists on system"""
    pass


def create_nb_user(email, password):
    try:
        User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        # Create a username (30 chars max) by joining email user and a counter.
        suffix_num = str(User.objects.count())
        username = '%s%s' % (email.split('@', 1)[0][:30 - len(suffix_num)], User.objects.count())
        username = username[:30]
        user = User.objects.create_user(username, email, password)
        return user
    else:
        raise UserAlreadyExists

