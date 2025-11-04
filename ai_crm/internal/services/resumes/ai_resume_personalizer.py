"""AI-powered resume personalization service."""

import json
import textwrap

from ai_crm.pkg import context
from ai_crm.pkg.clients.openai import client as openai_client
from ai_crm.pkg.logger import logger as logger_lib
from ai_crm.pkg.models.ai_crm import parsed_resume as parsed_resume_models
from ai_crm.pkg.models.exceptions import ai as ai_exceptions

logger = logger_lib.get_logger(__name__)

PERSONALIZATION_SYSTEM_PROMPT = textwrap.dedent(
    """
    You are an expert resume writer and career coach.
    Your task is to personalize a resume to match a specific job description.

    Guidelines:
    1. Enhance achievements to align with job requirements
    2. Highlight relevant skills and experience
    3. Adjust the professional summary to match the role
    4. Quantify achievements where possible
    5. Use action verbs and industry keywords
    6. Keep the tone professional and concise
    7. Maintain truthfulness - enhance, don't fabricate

    Return the personalized resume in the EXACT JSON structure as provided.
    """
).strip()


def _get_personalization_prompt(resume_data: dict, job_description: str) -> str:
    """Generate personalization prompt with schema."""
    schema_example = parsed_resume_models.ParsedResume.model_json_schema()

    return textwrap.dedent(
        f"""
        Job Description:
        {job_description}

        Current Resume Data:
        {json.dumps(resume_data, indent=2, default=str)}

        Expected Output JSON Schema:
        {schema_example}

        Please personalize this resume to match the job description.
        Enhance achievements, highlight relevant skills, and adjust the summary.
        Return the complete personalized resume in the EXACT JSON format shown in schema.
        """
    ).strip()


async def personalize_resume(
    context: context.AnyContext,
    parsed_resume: parsed_resume_models.ParsedResume,
    job_description: str,
) -> parsed_resume_models.ParsedResume:
    """Personalize resume based on job description using GPT.

    Args:
        context: Application context
        parsed_resume: Parsed resume structure
        job_description: Target job description

    Returns:
        Personalized resume structure

    Raises:
        ResumePersonalizationFailed: If personalization fails
    """
    try:
        logger.info(f"Personalizing resume for: {parsed_resume.name}")

        resume_dict = parsed_resume.model_dump(mode="json")
        user_prompt = _get_personalization_prompt(resume_dict, job_description)

        personalized_resume = await openai_client.personalize_with_gpt(
            response_model=parsed_resume_models.ParsedResume,
            system_prompt=PERSONALIZATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        logger.info("Successfully personalized resume with AI")
        return personalized_resume

    except Exception as e:
        logger.error(f"Resume personalization failed: {e}")
        if isinstance(e, ai_exceptions.BaseAPIException):
            raise
        raise ai_exceptions.ResumePersonalizationFailed from e
