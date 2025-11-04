"""Handler for AI-powered resume personalization."""

import io

from fastapi.responses import StreamingResponse

from ai_crm.internal.services.resumes import ai_resume_service
from ai_crm.pkg.context import web_context
from ai_crm.pkg.logger import logger as logger_lib
from ai_crm.pkg.models.ai_crm import ai_resume as ai_resume_models

logger = logger_lib.get_logger(__name__)


async def handle(
    context: web_context.WebContext,
    request: ai_resume_models.PersonalizeResumeRequest,
    user_id: str,
) -> StreamingResponse:
    """Handle AI resume personalization request.

    Returns:
        StreamingResponse with PDF file
    """
    logger.info(
        f"Starting AI resume personalization for resume_id: "
        f"{request.resume_id}, user: {user_id}"
    )

    new_resume = await ai_resume_service.personalize_and_save_resume(
        context=context,
        resume_id=request.resume_id,
        user_id=user_id,
        job_description=request.job_description,
    )

    file_content = await context.storage.get_file(new_resume.storage_path)

    logger.info(
        f"Returning AI-personalized resume: {new_resume.original_filename}"
    )

    return StreamingResponse(
        io.BytesIO(file_content),
        media_type=new_resume.mime_type,
        headers={
            "Content-Disposition": (
                f'attachment; filename="{new_resume.original_filename}"'
            )
        },
    )
