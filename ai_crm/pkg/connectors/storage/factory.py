from ai_crm.pkg.connectors.storage.base import BaseStorage
from ai_crm.pkg.connectors.storage.local import LocalStorage


def get_storage(storage_type: str = "local") -> BaseStorage:
    if storage_type == "local":
        return LocalStorage()
    elif storage_type == "s3":
        raise NotImplementedError(
            "S3 storage not yet configured. "
            "Update this factory when migrating to Yandex Cloud S3."
        )
    else:
        raise ValueError(f"Invalid storage type: {storage_type}")
