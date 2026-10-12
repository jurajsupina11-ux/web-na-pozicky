from django.contrib.auth.backends import ModelBackend


class BlockAwareModelBackend(ModelBackend):
    """Rovnaké ako štandardný ModelBackend, len navyše odmietne prihlásenie
    pre účty, ktoré administrátor zablokoval (User.is_blocked=True)."""

    def user_can_authenticate(self, user):
        if getattr(user, 'is_blocked', False):
            return False
        return super().user_can_authenticate(user)
