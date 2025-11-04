from io import BytesIO

from fastapi.responses import StreamingResponse

from ai_crm.internal.services.resumes import resumes as resumes_service
from ai_crm.pkg.context import web_context


async def handle(
    context: web_context.WebContext,
    resume_id: str,
    user_id: str,
) -> StreamingResponse:
    file_content, original_filename = await resumes_service.download_resume(
        context, resume_id, user_id
    )

    return StreamingResponse(
        BytesIO(file_content),
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{original_filename}"'
            )
        },
    )
