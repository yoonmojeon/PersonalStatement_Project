# myapp/routers.py

class MyAppRouter:
    route_app_labels = {'auth', 'sessions', 'admin', 'contenttypes', 'myapp'}  # myapp에 사용자 및 자기소개서 모델 포함

    def db_for_read(self, model, **hints):
        """읽기 작업에 사용할 데이터베이스를 지정합니다."""
        if model._meta.app_label in self.route_app_labels:
            if hasattr(model, 'use_mysql') and model.use_mysql:
                return 'mysql_db'
            else:
                return 'default'
        return None

    def db_for_write(self, model, **hints):
        """쓰기 작업에 사용할 데이터베이스를 지정합니다."""
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        """두 객체 간의 관계를 허용할지 결정합니다."""
        if obj1._meta.app_label in self.route_app_labels and obj2._meta.app_label in self.route_app_labels:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """모델의 마이그레이션을 허용할 데이터베이스를 지정합니다."""
        if app_label in self.route_app_labels:
            if db == 'mysql_db':
                return model_name in ('company',)  # MySQL에만 마이그레이션되는 모델
            elif db == 'default':
                return model_name not in ('company',)  # SQLite에 마이그레이션되는 나머지 모델
        return None
