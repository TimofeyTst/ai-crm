"""Base storage interface for file operations."""

from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    async def save_file(self, file_path: str, file_content: bytes) -> str:
        """Save file to storage.

        Args:
            file_path: Relative path where file should be saved
            file_content: File content as bytes

        Returns:
            Storage path of saved file
        """
        pass

    @abstractmethod
    async def get_file(self, file_path: str) -> bytes:
        """Retrieve file from storage.

        Args:
            file_path: Path to file in storage

        Returns:
            File content as bytes
        """
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """Delete file from storage.

        Args:
            file_path: Path to file in storage

        Returns:
            True if deleted successfully
        """
        pass

    @abstractmethod
    async def file_exists(self, file_path: str) -> bool:
        """Check if file exists in storage.

        Args:
            file_path: Path to file in storage

        Returns:
            True if file exists
        """
        pass

    @abstractmethod
    def get_storage_type(self) -> str:
        """Get storage type identifier.

        Returns:
            Storage type (e.g., 'local', 's3')
        """
        pass
