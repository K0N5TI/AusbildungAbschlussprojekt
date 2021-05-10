class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    TEMPLATES_AUTO_RELOAD = True
    

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True