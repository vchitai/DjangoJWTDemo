class AuthenticationRouter:
    def db_for_read(self, model, **hint):
        if model._meta.app_label == 'client_auth':
            return 'authentication'
        return None

    def db_for_write(self, model, **hint):
        if model._meta.app_label == 'client_auth':
            return 'authentication'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'client_auth':
            return 'authentication'
        return None
