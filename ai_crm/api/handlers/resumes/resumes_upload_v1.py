from fastapi import UploadFile

from ai_crm.internal.services.resumes import resumes as resumes_service
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import resume as resume_models


async def handle(
    context: web_context.WebContext,
    file: UploadFile,
    user_id: str,
    title: str | None = None,
    description: str | None = None,
) -> resume_models.ResumeUploadResponse:
    file_content = await file.read()

    resume = await resumes_service.upload_resume(
        context=context,
        user_id=user_id,
        file_content=file_content,
        original_filename=file.filename or "no_name_resume.pdf",
        title=title,
        description=description,
    )

    return resume_models.ResumeUploadResponse(
        id=resume.id,
        filename=resume.filename,
        original_filename=resume.original_filename,
        file_size=resume.file_size,
        download_url=f"/api/resumes/{resume.id}/download",
        created_at=resume.created_at,
    )
