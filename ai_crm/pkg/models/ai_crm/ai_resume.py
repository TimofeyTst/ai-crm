"""Models for AI resume personalization endpoints."""

from pydantic import Field

from ai_crm.pkg.models.base import model as base_models


class PersonalizeResumeRequest(base_models.BaseModel):
    resume_id: str = Field(
        description="Resume ID to personalize",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    job_description: str = Field(
        description="Job description to tailor resume for",
        example="We are looking for a Senior Software Engineer with 5+ years of experience...",
    )


class PersonalizeResumeResponse(base_models.BaseModel):
    resume_id: str = Field(
        description="Original resume ID",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    personalized_resume_filename: str = Field(
        description="Generated resume filename",
        example="John_Doe_Resume_Personalized.docx",
    )
    download_url: str = Field(
        description="URL to download personalized resume",
        example="/api/v1/resumes/ai/download/temp_uuid.docx",
    )
