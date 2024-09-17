class AppDbRouter:
    route_app_labels = {'App_db'}

    def db_for_read(self, model, **hints):
        return 'default' if model._meta.app_label in self.route_app_labels else None 

    def db_for_write(self, model, **hints):
        return 'default' if model._meta.app_label in self.route_app_labels else None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default' if app_label in self.route_app_labels else None 


class IntelliSyncDbRouter:
    route_app_labels = {'auth', 'contenttypes', 'sessions', 'admin', 'IntelliSync_db'}

    def db_for_read(self, model, **hints):
        return 'intellisync_db' if model._meta.app_label in self.route_app_labels else None 

    def db_for_write(self, model, **hints):
        return 'intellisync_db' if model._meta.app_label in self.route_app_labels else None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'intellisync_db' if app_label in self.route_app_labels else None 


class HRMSDbRouter:
    route_app_labels = {'HRMS_db'}

    def db_for_read(self, model, **hints):
        return 'hrms_db' if model._meta.app_label in self.route_app_labels else None 

    def db_for_write(self, model, **hints):
        return 'hrms_db' if model._meta.app_label in self.route_app_labels else None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'hrms_db' if app_label in self.route_app_labels else None 


class PayrollDbRouter:
    route_app_labels = {'Payroll_db'}

    def db_for_read(self, model, **hints):
        return 'payroll_db' if model._meta.app_label in self.route_app_labels else None 

    def db_for_write(self, model, **hints):
        return 'payroll_db' if model._meta.app_label in self.route_app_labels else None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'payroll_db' if app_label in self.route_app_labels else None 


class ERPDbRouter:
    route_app_labels = {'ERP_db'}

    def db_for_read(self, model, **hints):
        return 'erp_db' if model._meta.app_label in self.route_app_labels else None 

    def db_for_write(self, model, **hints):
        return 'erp_db' if model._meta.app_label in self.route_app_labels else None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'erp_db' if app_label in self.route_app_labels else None 


