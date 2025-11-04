from datetime import datetime
from pathlib import Path
import uuid

from ai_crm.internal.repository.postgresql import resumes as resumes_repository
from ai_crm.pkg import context
from ai_crm.pkg.connectors.postgresql import psql
from ai_crm.pkg.logger import logger as logger_lib
from ai_crm.pkg.models.ai_crm import resume as resume_models
from ai_crm.pkg.models.exceptions import postgres as postgres_exceptions
from ai_crm.pkg.models.exceptions import resumes as resume_exceptions

logger = logger_lib.get_logger(__name__)

# TODO: Encrypt/Decrypt file contents

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_MIME_TYPES = ["application/pdf"]
ALLOWED_EXTENSIONS = [".pdf"]


async def upload_resume(
    context: context.AnyContext,
    user_id: str,
    file_content: bytes,
    original_filename: str,
    title: str | None = None,
    description: str | None = None,
) -> resume_models.Resume:
    """Upload resume file and create metadata record.

    Raises:
        InvalidFileType: If file type is not PDF
        FileTooLarge: If file size exceeds limit
    """
    file_size = len(file_content)
    if file_size > MAX_FILE_SIZE:
        logger.warning(
            f"File too large: {file_size} bytes (max {MAX_FILE_SIZE})"
        )
        raise resume_exceptions.FileTooLarge

    # Validate file extension
    file_ext = Path(original_filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        logger.warning(f"Invalid file extension: {file_ext}")
        raise resume_exceptions.InvalidFileType

    unique_id = uuid.uuid4()
    filename = f"{unique_id}{file_ext}"

    # Generate storage path: resumes/YYYY/MM/uuid.pdf
    now = datetime.now()
    storage_path = f"{now.year:04d}/{now.month:02d}/{filename}"

    async with psql.get_connection(context) as _:  # Open transaction
        resume = await resumes_repository.create_resume(
            context=context,
            user_id=user_id,
            filename=filename,
            original_filename=original_filename,
            file_size=file_size,
            mime_type="application/pdf",
            storage_path=storage_path,
            storage_type=context.storage.get_storage_type(),
            media_type="cv",
            title=title,
            description=description,
        )
        await context.storage.save_file(storage_path, file_content)

    logger.info(f"Resume uploaded successfully: {resume.id} for user {user_id}")
    return resume


async def download_resume(
    context: context.AnyContext, resume_id: str, user_id: str
) -> tuple[bytes, str]:
    """Download resume file.

    Returns:
        Tuple of (file_content, original_filename)

    Raises:
        ResumeNotFound: If resume doesn't exist
        ResumeAccessDenied: If user doesn't own the resume
        FileNotFoundInStorage: If file doesn't exist in storage
    """
    # Get resume metadata
    try:
        resume = await resumes_repository.get_resume_by_id(context, resume_id)
    except postgres_exceptions.EmptyResult as e:
        raise resume_exceptions.ResumeNotFound from e

    # Check access rights
    if resume.user_id != user_id:
        logger.warning(
            f"Access denied: User {user_id} "
            f"attempted to access resume {resume_id}"
        )
        raise resume_exceptions.ResumeAccessDenied

    if not resume.is_active:
        raise resume_exceptions.ResumeNotFound

    try:
        file_content = await context.storage.get_file(resume.storage_path)
    except FileNotFoundError as e:
        logger.error(f"File not found in storage: {resume.storage_path}")
        raise resume_exceptions.FileNotFoundInStorage from e

    logger.info(f"Resume downloaded: {resume_id} by user {user_id}")
    return file_content, resume.original_filename


async def get_user_resumes(
    context: context.AnyContext, user_id: str
) -> list[resume_models.Resume]:
    resumes = await resumes_repository.get_user_resumes(
        context, user_id, only_active=True
    )
    logger.info(f"Retrieved {len(resumes)} resumes for user {user_id}")
    return resumes


async def delete_resume(
    context: context.AnyContext, resume_id: str, user_id: str
) -> bool:
    """Delete resume (soft delete).

    Returns:
        True if deleted successfully

    Raises:
        ResumeNotFound: If resume doesn't exist
        ResumeAccessDenied: If user doesn't own the resume
    """
    # Get resume metadata
    try:
        resume = await resumes_repository.get_resume_by_id(context, resume_id)
    except postgres_exceptions.EmptyResult as e:
        raise resume_exceptions.ResumeNotFound from e

    if resume.user_id != user_id:
        logger.warning(
            f"Access denied: User {user_id} "
            f"attempted to delete resume {resume_id}"
        )
        raise resume_exceptions.ResumeAccessDenied

    success = await resumes_repository.delete_resume(context, resume_id)

    if success:
        logger.info(f"Resume deleted: {resume_id} by user {user_id}")

    return success
