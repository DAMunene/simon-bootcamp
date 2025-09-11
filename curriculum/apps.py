from django.apps import AppConfig


class CurriculumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'curriculum'
    verbose_name = 'Curriculum Management'
    
    def ready(self):
        """Import signal handlers when the app is ready"""
        try:
            import curriculum.signals
        except ImportError:
            pass