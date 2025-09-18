from ai_crm.pkg.models.base import enum as base_enum

class LoggerLevel(str, base_enum.BaseEnum):
    WARNING = "WARNING"
    INFO = "INFO"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"
    NOTSET = "NOTSET"
