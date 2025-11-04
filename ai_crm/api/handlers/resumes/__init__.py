from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from starlette import status

from ai_crm.api.handlers.resumes import (
    resumes_ai_personalize_v1,
    resumes_delete_v1,
    resumes_download_v1,
    resumes_list_v1,
    resumes_upload_v1,
)
from ai_crm.api.middlewares import jwt_auth
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import ai_resume as ai_resume_models
from ai_crm.pkg.models.ai_crm import resume as resume_models
from ai_crm.pkg.models.ai_crm import user as user_models
from ai_crm.pkg.models.exceptions import ai as ai_exceptions
from ai_crm.pkg.models.exceptions import resumes as resume_exceptions

resume_router = APIRouter(
    prefix="/v1/resumes",
    tags=["Resumes"],
    responses={
        **resume_exceptions.ResumeNotFound.generate_openapi(),
        **resume_exceptions.ResumeAccessDenied.generate_openapi(),
        **resume_exceptions.InvalidFileType.generate_openapi(),
        **resume_exceptions.FileTooLarge.generate_openapi(),
        **ai_exceptions.AIServiceError.generate_openapi(),
        **ai_exceptions.ResumeParsingFailed.generate_openapi(),
        **ai_exceptions.ResumePersonalizationFailed.generate_openapi(),
    },
)


@resume_router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    description="Upload resume PDF file",
    response_model=resume_models.ResumeUploadResponse,
)
async def _resumes_upload_v1(
    file: UploadFile = File(..., description="PDF file to upload"),
    title: str | None = Form(None, description="Resume title"),
    description: str | None = Form(None, description="Resume description"),
    current_user: user_models.User = Depends(jwt_auth.get_current_user),
    web_context: web_context.WebContext = Depends(
        web_context.get_web_context_dependency()
    ),
):
    return await resumes_upload_v1.handle(
        web_context, file, current_user.id, title, description
    )


@resume_router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    description="Get all user's resumes",
    response_model=list[resume_models.ResumeListResponse],
)
async def _resumes_list_v1(
    current_user: user_models.User = Depends(jwt_auth.get_current_user),
    web_context: web_context.WebContext = Depends(
        web_context.get_web_context_dependency()
    ),
):
    return await resumes_list_v1.handle(web_context, current_user.id)


@resume_router.get(
    "/download/{resume_id}",
    status_code=status.HTTP_200_OK,
    description="Download resume PDF file",
    response_class=StreamingResponse,
)
async def _resumes_download_v1(
    resume_id: str,
    current_user: user_models.User = Depends(jwt_auth.get_current_user),
    web_context: web_context.WebContext = Depends(
        web_context.get_web_context_dependency()
    ),
):
    return await resumes_download_v1.handle(
        web_context, resume_id, current_user.id
    )


@resume_router.delete(
    "/delete/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete resume",
)
async def _resumes_delete_v1(
    resume_id: str,
    current_user: user_models.User = Depends(jwt_auth.get_current_user),
    web_context: web_context.WebContext = Depends(
        web_context.get_web_context_dependency()
    ),
):
    return await resumes_delete_v1.handle(
        web_context, resume_id, current_user.id
    )


@resume_router.post(
    "/ai/personalize",
    status_code=status.HTTP_200_OK,
    description="Personalize resume using AI based on job description",
    response_class=StreamingResponse,
)
async def _resumes_ai_personalize_v1(
    request: ai_resume_models.PersonalizeResumeRequest,
    current_user: user_models.User = Depends(jwt_auth.get_current_user),
    web_context: web_context.WebContext = Depends(
        web_context.get_web_context_dependency()
    ),
):
    return await resumes_ai_personalize_v1.handle(
        web_context, request, current_user.id
    )
