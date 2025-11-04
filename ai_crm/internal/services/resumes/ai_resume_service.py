"""Service for AI-powered resume operations."""

from datetime import datetime
import uuid

from ai_crm.internal.repository.postgresql import resumes as resumes_repository
from ai_crm.internal.services.resumes import (
    ai_resume_parser,
    ai_resume_personalizer,
    resume_generator,
)
from ai_crm.pkg import context
from ai_crm.pkg.logger import logger as logger_lib
from ai_crm.pkg.models.ai_crm import resume as resume_models
from ai_crm.pkg.models.exceptions import postgres as postgres_exceptions
from ai_crm.pkg.models.exceptions import resumes as resume_exceptions

logger = logger_lib.get_logger(__name__)


async def personalize_and_save_resume(
    context: context.AnyContext,
    resume_id: str,
    user_id: str,
    job_description: str,
) -> resume_models.Resume:
    """Personalize resume with AI and save as new resume.

    Args:
        context: Application context
        resume_id: Original resume ID
        user_id: User ID
        job_description: Job description for personalization

    Returns:
        New AI-personalized resume record

    Raises:
        ResumeNotFound: If resume doesn't exist
        ResumeAccessDenied: If user doesn't own the resume
    """
    # TODO: вынести в сервис get_resume_by_id
    try:
        resume_metadata = await resumes_repository.get_resume_by_id(
            context, resume_id
        )
    except postgres_exceptions.EmptyResult as e:
        raise resume_exceptions.ResumeNotFound from e

    if resume_metadata.user_id != user_id:
        logger.warning(
            f"Access denied: User {user_id} attempted to personalize "
            f"resume {resume_id}"
        )
        raise resume_exceptions.ResumeAccessDenied

    if not resume_metadata.is_active:
        raise resume_exceptions.ResumeNotFound

    file_content = await context.storage.get_file(resume_metadata.storage_path)

    logger.info("Step 1/5: Parsing resume with GPT...")
    parsed_resume = await ai_resume_parser.parse_pdf_resume(
        context, file_content
    )

    logger.info("Step 2/5: Personalizing resume with GPT...")
    personalized_resume = await ai_resume_personalizer.personalize_resume(
        context, parsed_resume, job_description
    )

    logger.info("Step 3/5: Generating DOCX resume...")
    docx_bytes = await resume_generator.generate_docx_resume(
        context, personalized_resume
    )

    unique_id = uuid.uuid4()
    filename = f"{unique_id}.docx"
    original_filename = (
        f"{personalized_resume.name.replace(' ', '_')}_Resume_AI.docx"
    )

    now = datetime.now()
    storage_path = f"{now.year:04d}/{now.month:02d}/{filename}"

    logger.info("Step 4/5: Saving DOCX file to storage...")
    await context.storage.save_file(storage_path, docx_bytes)

    logger.info("Step 5/5: Creating database record...")
    new_resume = await resumes_repository.create_resume(
        context=context,
        user_id=user_id,
        filename=filename,
        original_filename=original_filename,
        file_size=len(docx_bytes),
        mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        storage_path=storage_path,
        storage_type=context.storage.get_storage_type(),
        media_type="ai-cv",
        title=f"AI Personalized - {personalized_resume.position or 'Resume'}",
        description=f"Personalized for: {job_description[:100]}...",
    )

    logger.info(f"AI-personalized resume saved: {new_resume.id}")
    return new_resume
