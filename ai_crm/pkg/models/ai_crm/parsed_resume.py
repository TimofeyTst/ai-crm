from datetime import date

from pydantic import Field

from ai_crm.pkg.models.base import model as base_models


class Education(base_models.BaseModel):
    institution: str = Field(description="Education institution name")
    degree: str | None = Field(None, description="Degree or field of study")
    from_date: date | None = Field(None, description="Start date")
    to_date: date | None = Field(None, description="End date (None if current)")
    description: str | None = Field(None, description="Additional details")


class ProfessionalExperience(base_models.BaseModel):
    company_name: str = Field(description="Company name")
    position: str = Field(description="Job title/position")
    hired_date: date | None = Field(None, description="Start date")
    fired_date: date | None = Field(
        None, description="End date (None if currently employed)"
    )
    achievements: list[str] = Field(
        default_factory=list, description="List of key achievements"
    )


class Certification(base_models.BaseModel):
    name: str = Field(description="Certification or training name")
    description: str | None = Field(None, description="Additional details")
    date_obtained: date | None = Field(None, description="Date when obtained")


class Skills(base_models.BaseModel):
    tech_stack: str | None = Field(
        None, description="Technical skills and tools"
    )
    languages: str | None = Field(
        None, description="Programming or spoken languages"
    )
    soft_skills: str | None = Field(None, description="Soft skills")


class ParsedResume(base_models.BaseModel):
    name: str = Field(description="Full name")
    position: str | None = Field(
        None, description="Desired or current position"
    )
    email: str | None = Field(None, description="Email address")
    linkedin: str | None = Field(None, description="LinkedIn URL")
    phone: str | None = Field(None, description="Phone number")
    summary: str | None = Field(None, description="Professional summary")
    education: list[Education] = Field(
        default_factory=list, description="Education history"
    )
    professional_experience: list[ProfessionalExperience] = Field(
        default_factory=list, description="Work experience"
    )
    certifications: list[Certification] = Field(
        default_factory=list,
        description="Certifications and additional training",
    )
    skills: Skills = Field(
        default_factory=Skills, description="Skills overview"
    )
