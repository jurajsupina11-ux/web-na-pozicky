"""Nezávislá záloha databázy mimo Render (pg_dump -> S3-kompatibilné úložisko).

Dôvod: Render robí automatické zálohy na platenom pláne, ale tie sú viazané na
samotný Render účet - ak by nastal problém priamo s Renderom (zmazaný účet,
výpadok regiónu a pod.), prídeme aj o zálohy. Táto úloha preto exportuje
databázu cez `pg_dump` a nahrá ju na nezávislé úložisko (akékoľvek S3-kompatibilné
- AWS S3, Backblaze B2, Cloudflare R2...), nastavené cez env premenné:

    BACKUP_S3_BUCKET, BACKUP_S3_ENDPOINT_URL, BACKUP_S3_ACCESS_KEY,
    BACKUP_S3_SECRET_KEY, BACKUP_S3_REGION (voliteľné)

Spúšťať pravidelne (napr. raz týždenne) cez Render Cron Job:
    python manage.py backup_database
"""
import datetime
import os
import subprocess
import tempfile

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Exportuje databázu cez pg_dump a nahrá ju na nezávislé S3-kompatibilné úložisko.'

    def handle(self, *args, **options):
        db = settings.DATABASES['default']
        if 'postgresql' not in db.get('ENGINE', ''):
            self.stdout.write(self.style.WARNING(
                'Záloha cez pg_dump je podporovaná len pre PostgreSQL - preskakujem (lokálne SQLite).',
            ))
            return

        bucket = os.environ.get('BACKUP_S3_BUCKET')
        if not bucket:
            self.stdout.write(self.style.WARNING(
                'BACKUP_S3_BUCKET nie je nastavené - záloha sa nenahrá nikam, preskakujem. '
                'Nastav BACKUP_S3_BUCKET/BACKUP_S3_ENDPOINT_URL/BACKUP_S3_ACCESS_KEY/BACKUP_S3_SECRET_KEY.',
            ))
            return

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'pozicky_backup_{timestamp}.dump'

        with tempfile.TemporaryDirectory() as tmp_dir:
            dump_path = os.path.join(tmp_dir, filename)
            env = os.environ.copy()
            env['PGPASSWORD'] = db.get('PASSWORD', '')
            cmd = [
                'pg_dump', '-Fc',
                '-h', db.get('HOST', 'localhost'),
                '-p', str(db.get('PORT', 5432)),
                '-U', db.get('USER', ''),
                '-d', db.get('NAME', ''),
                '-f', dump_path,
            ]
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            if result.returncode != 0:
                self.stderr.write(self.style.ERROR(f'pg_dump zlyhal: {result.stderr}'))
                return

            self._upload_to_s3(dump_path, filename, bucket)
        self.stdout.write(self.style.SUCCESS(f'Záloha {filename} bola vytvorená a nahraná.'))

    def _upload_to_s3(self, dump_path, filename, bucket):
        import boto3

        client = boto3.client(
            's3',
            endpoint_url=os.environ.get('BACKUP_S3_ENDPOINT_URL') or None,
            aws_access_key_id=os.environ.get('BACKUP_S3_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('BACKUP_S3_SECRET_KEY'),
            region_name=os.environ.get('BACKUP_S3_REGION') or None,
        )
        client.upload_file(dump_path, bucket, f'backups/{filename}')
