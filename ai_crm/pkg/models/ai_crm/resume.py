from datetime import datetime

from pydantic import Field

from ai_crm.pkg.models.base import model as base_models


class ResumeFields:
    id: str = Field(
        description="Resume id (UUID)",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    user_id: str = Field(
        description="User id who owns the resume (UUID)",
        example="123e4567-e89b-12d3-a456-426614174001",
    )
    filename: str = Field(
        description="Stored filename", example="uuid-filename.pdf"
    )
    original_filename: str = Field(
        description="Original filename", example="my_resume.pdf"
    )
    file_size: int = Field(description="File size in bytes", example=102400)
    mime_type: str = Field(description="MIME type", example="application/pdf")
    storage_path: str = Field(
        description="Storage path", example="resumes/2024/01/uuid.pdf"
    )
    storage_type: str = Field(description="Storage type", example="local")
    title: str | None = Field(
        None, description="Resume title", example="Software Engineer Resume"
    )
    description: str | None = Field(
        None, description="Resume description", example="My latest resume"
    )
    is_active: bool = Field(description="Is active", example=True)
    created_at: datetime = Field(
        description="Created at", example=datetime.now()
    )
    updated_at: datetime = Field(
        description="Updated at", example=datetime.now()
    )


class Resume(base_models.BaseModel):
    """Resume model with full metadata."""

    id: str = ResumeFields.id
    user_id: str = ResumeFields.user_id
    filename: str = ResumeFields.filename
    original_filename: str = ResumeFields.original_filename
    file_size: int = ResumeFields.file_size
    mime_type: str = ResumeFields.mime_type
    storage_path: str = ResumeFields.storage_path
    storage_type: str = ResumeFields.storage_type
    title: str | None = ResumeFields.title
    description: str | None = ResumeFields.description
    is_active: bool = ResumeFields.is_active
    created_at: datetime = ResumeFields.created_at
    updated_at: datetime = ResumeFields.updated_at


class ResumeUploadRequest(base_models.BaseModel):
    """Request model for resume upload metadata."""

    title: str | None = Field(
        None, description="Resume title", example="Software Engineer Resume"
    )
    description: str | None = Field(
        None, description="Resume description", example="My latest resume"
    )


class ResumeUploadResponse(base_models.BaseModel):
    """Response model for resume upload."""

    id: str = Field(
        description="Resume id (UUID)",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    filename: str = Field(
        description="Stored filename", example="uuid-filename.pdf"
    )
    original_filename: str = Field(
        description="Original filename", example="my_resume.pdf"
    )
    file_size: int = Field(description="File size in bytes", example=102400)
    download_url: str = Field(
        description="Download URL", example="/api/resumes/1/download"
    )
    created_at: datetime = Field(
        description="Created at", example=datetime.now()
    )


class ResumeListResponse(base_models.BaseModel):
    """Resume list item response."""

    id: str = ResumeFields.id
    original_filename: str = ResumeFields.original_filename
    file_size: int = ResumeFields.file_size
    title: str | None = ResumeFields.title
    description: str | None = ResumeFields.description
    created_at: datetime = ResumeFields.created_at
    download_url: str = Field(
        description="Download URL", example="/api/resumes/1/download"
    )
