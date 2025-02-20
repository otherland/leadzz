class BigQueryRouter:
    """
    Router to handle BigQuery models vs PostgreSQL models
    """
    def db_for_read(self, model, **hints):
        # Log the model being accessed
        print(f"Routing read for model: {model._meta.model_name}")
        if model._meta.model_name == 'bigquerycontact':
            return None
        return 'default'

    def db_for_write(self, model, **hints):
        # Prevent writes to BigQuery model
        if model._meta.model_name == 'bigquerycontact':
            return None
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Only allow migrations for non-BigQuery models
        if model_name == 'bigquerycontact':
            return False
        return True 