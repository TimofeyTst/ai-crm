"""Service for AI-powered resume operations."""

from datetime import datetime
import uuid

from ai_crm.internal.repository.postgresql import resumes as resumes_repository
from ai_crm.internal.services.resumes import (
    ai_resume_parser,
    ai_resume_personalizer,
    resume_generator,
    resumes,
)
from ai_crm.pkg import context
from ai_crm.pkg.logger import logger as logger_lib
from ai_crm.pkg.models.ai_crm import resume as resume_models

logger = logger_lib.get_logger(__name__)


async def personalize_and_save_resume(
    context: context.AnyContext,
    resume_id: str,
    user_id: str,
    job_description: str,
) -> resume_models.Resume:
    """Personalize resume with AI and save as new resume.

    Workflow:
    1. Parse original resume with GPT
    2. Personalize based on job description
    3. Generate DOCX file
    4. Save to storage
    5. Create database record (media_type='ai-cv')
    6. Return DOCX file

    Returns:
        New AI-personalized resume record

    Raises:
        ResumeNotFound: If resume doesn't exist
        ResumeAccessDenied: If user doesn't own the resume
    """
    resume_metadata = await resumes.get_resume_by_id(
        context, resume_id, user_id
    )
    file_content = await context.storage.get_file(resume_metadata.storage_path)

    logger.info("Step 1/5: Parsing resume with GPT...")
    parsed_resume = await ai_resume_parser.parse_pdf_resume(
        context, file_content
    )

    logger.info("Step 2/5: Personalizing resume with GPT...")
    personalized_resume = await ai_resume_personalizer.personalize_resume(
        context, parsed_resume, job_description
    )

    logger.info("Step 3/6: Generating DOCX resume...")
    docx_bytes = await resume_generator.generate_docx_resume(
        context, personalized_resume
    )

    logger.info("Step 4/6: Generating PDF resume...")
    pdf_bytes = await resume_generator.generate_pdf_resume(
        context, personalized_resume
    )

    unique_id = uuid.uuid4()
    now = datetime.now()
    base_name = personalized_resume.name.replace(" ", "_")

    docx_filename = f"{unique_id}.docx"
    pdf_filename = f"{unique_id}.pdf"
    docx_storage_path = f"{now.year:04d}/{now.month:02d}/{docx_filename}"
    pdf_storage_path = f"{now.year:04d}/{now.month:02d}/{pdf_filename}"

    logger.info("Step 5/6: Saving files to storage...")
    await context.storage.save_file(docx_storage_path, docx_bytes)
    await context.storage.save_file(pdf_storage_path, pdf_bytes)

    logger.info("Step 6/6: Creating database records...")
    pdf_resume = await resumes_repository.create_resume(
        context=context,
        user_id=user_id,
        filename=pdf_filename,
        original_filename=f"{base_name}_Resume_AI.pdf",
        file_size=len(pdf_bytes),
        mime_type="application/pdf",
        storage_path=pdf_storage_path,
        storage_type=context.storage.get_storage_type(),
        media_type="ai-cv",
        title=f"AI Personalized - {personalized_resume.position or 'Resume'}",
        description=f"Personalized for: {job_description[:100]}...",
    )

    docx_resume = await resumes_repository.create_resume(
        context=context,
        user_id=user_id,
        filename=docx_filename,
        original_filename=f"{base_name}_Resume_AI.docx",
        file_size=len(docx_bytes),
        mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        storage_path=docx_storage_path,
        storage_type=context.storage.get_storage_type(),
        media_type="ai-cv",
        title=f"AI Personalized - {personalized_resume.position or 'Resume'} (DOCX)",
        description=f"Personalized for: {job_description[:100]}...",
    )

    logger.info(
        f"AI-personalized resumes saved - PDF: {pdf_resume.id}, DOCX: {docx_resume.id}"
    )
    return pdf_resume
