import random
import string

from django.db import migrations


def _assign_security_codes(apps, schema_editor):
    """Doplní bezpečnostný kód aj dlžníkom (migrácia 0007 ho pôvodne priradila
    len investorom) - teraz ho potrebujú aj dlžníci na potvrdenie zmeny hesla."""
    User = apps.get_model('users', 'User')
    for user in User.objects.filter(security_code=''):
        user.security_code = ''.join(random.choices(string.digits, k=8))
        user.save(update_fields=['security_code'])


def _noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_security_code'),
    ]

    operations = [
        migrations.RunPython(_assign_security_codes, _noop),
    ]
