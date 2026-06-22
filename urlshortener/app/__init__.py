from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import os
        if os.environ.get('VERCEL'):
            from django.core.management import call_command
            try:
                call_command('migrate', '--run-syncdb', verbosity=0)
            except Exception:
                pass