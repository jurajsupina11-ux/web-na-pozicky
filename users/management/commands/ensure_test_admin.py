from django.core.management.base import BaseCommand

from users.models import User

#: Testovací admin účet - slúži len na manuálne overenie admin náhľadu
#: (impersonation) na produkcii. Nemusí byť nijako overený, nepoužíva sa
#: na reálnu správu platformy.
TEST_ADMIN_USERNAME = 'admin'
TEST_ADMIN_PASSWORD = 'AdminTest2026!'
TEST_ADMIN_EMAIL = 'admin@pozickypredlznikov.sk'


class Command(BaseCommand):
    help = 'Vytvorí (ak ešte neexistuje) testovací superuser účet pre admin náhľad.'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username=TEST_ADMIN_USERNAME,
            defaults={
                'email': TEST_ADMIN_EMAIL,
                'is_staff': True,
                'is_superuser': True,
                'role': User.Role.BOTH,
            },
        )
        if created:
            user.set_password(TEST_ADMIN_PASSWORD)
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f'Testovací admin účet "{TEST_ADMIN_USERNAME}" bol vytvorený.',
            ))
        else:
            # Pre istotu zabezpečí, že účet má stále admin práva aj heslo,
            # aj keby bol medzičasom v DB zmenený.
            user.is_staff = True
            user.is_superuser = True
            user.set_password(TEST_ADMIN_PASSWORD)
            user.save()
            self.stdout.write(self.style.WARNING(
                f'Testovací admin účet "{TEST_ADMIN_USERNAME}" už existoval - heslo/práva boli obnovené.',
            ))
