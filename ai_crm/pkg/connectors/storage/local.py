"""Local filesystem storage implementation."""

from pathlib import Path

import aiofiles

from ai_crm.pkg.configuration import settings
from ai_crm.pkg.connectors.storage.base import BaseStorage
from ai_crm.pkg.logger import logger as logger_lib

logger = logger_lib.get_logger(__name__)


class LocalStorage(BaseStorage):
    """Local filesystem storage implementation."""

    def __init__(self, base_path: Path | None = None):
        """Initialize local storage.

        Args:
            base_path: Base directory for file storage.
                      Defaults to DATA_VOLUME from settings.
        """
        self.base_path = (
            base_path or settings.ai_crm_env.DATA_VOLUME / "resumes"
        )
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"LocalStorage initialized at {self.base_path}")

    async def save_file(self, file_path: str, file_content: bytes) -> str:
        full_path = self.base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(full_path, "wb") as f:
            await f.write(file_content)

        logger.info(f"File saved to local storage: {file_path}")
        return file_path

    async def get_file(self, file_path: str) -> bytes:
        full_path = self.base_path / file_path

        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        async with aiofiles.open(full_path, "rb") as f:
            content = await f.read()

        logger.info(f"File retrieved from local storage: {file_path}")
        return content

    async def delete_file(self, file_path: str) -> bool:
        full_path = self.base_path / file_path

        if not full_path.exists():
            logger.warning(f"File not found for deletion: {file_path}")
            return False

        full_path.unlink()
        logger.info(f"File deleted from local storage: {file_path}")
        return True

    async def file_exists(self, file_path: str) -> bool:
        full_path = self.base_path / file_path
        return full_path.exists()

    def get_storage_type(self) -> str:
        return "local"
