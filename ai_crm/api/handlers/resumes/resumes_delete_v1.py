from fastapi.responses import Response
from starlette import status

from ai_crm.internal.services.resumes import resumes as resumes_service
from ai_crm.pkg.context import web_context


async def handle(
    context: web_context.WebContext,
    resume_id: str,
    user_id: str,
) -> Response:
    await resumes_service.delete_resume(context, resume_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
