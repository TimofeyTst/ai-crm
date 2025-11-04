from ai_crm.internal.services.resumes import resumes as resumes_service
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import resume as resume_models


async def handle(
    context: web_context.WebContext,
    user_id: str,
) -> list[resume_models.ResumeListResponse]:
    resumes = await resumes_service.get_user_resumes(context, user_id)

    return [
        resume_models.ResumeListResponse(
            id=resume.id,
            original_filename=resume.original_filename,
            file_size=resume.file_size,
            title=resume.title,
            description=resume.description,
            created_at=resume.created_at,
            download_url=f"/api/resumes/{resume.id}/download",
        )
        for resume in resumes
    ]
