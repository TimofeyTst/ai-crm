"""AI-powered resume parsing service using GPT."""

import textwrap

import PyPDF2

from ai_crm.pkg import context
from ai_crm.pkg.clients.openai import client as openai_client
from ai_crm.pkg.logger import logger as logger_lib
from ai_crm.pkg.models.ai_crm import parsed_resume as parsed_resume_models
from ai_crm.pkg.models.exceptions import ai as ai_exceptions

logger = logger_lib.get_logger(__name__)

SYSTEM_PROMPT = textwrap.dedent(
    """
    You are an expert resume parser.
    Extract structured information from resumes accurately.
    Return data in valid JSON format matching the EXACT schema provided.
    For dates, use ISO format (YYYY-MM-DD).
    If information is not available, use null.
    """
).strip()


def _get_user_prompt(content: str) -> str:
    """Generate user prompt with JSON schema example."""
    schema_example = parsed_resume_models.ParsedResume.model_json_schema()

    return textwrap.dedent(
        f"""
        Parse the following resume and extract all relevant information.

        Expected JSON Schema:
        {schema_example}

        Example structure:
        {{
            "name": "John Doe",
            "position": "Senior Software Engineer",
            "email": "john@example.com",
            "linkedin": "https://linkedin.com/in/johndoe",
            "phone": "+1-234-567-8900",
            "summary": "Experienced software engineer...",
            "education": [
                {{
                    "institution": "University Name",
                    "degree": "Bachelor of Science in Computer Science",
                    "from_date": "2015-09-01",
                    "to_date": "2019-06-01",
                    "description": "GPA: 3.8/4.0"
                }}
            ],
            "professional_experience": [
                {{
                    "company_name": "Tech Corp",
                    "position": "Senior Software Engineer",
                    "hired_date": "2020-01-15",
                    "fired_date": null,
                    "achievements": [
                        "Led team of 5 engineers",
                        "Increased performance by 40%"
                    ]
                }}
            ],
            "certifications": [
                {{
                    "name": "AWS Certified Solutions Architect",
                    "description": "Professional level certification",
                    "date_obtained": "2021-06-15"
                }}
            ],
            "skills": {{
                "tech_stack": "Python, FastAPI, PostgreSQL, Docker, AWS",
                "languages": "English (Native), Spanish (Professional)",
                "soft_skills": "Leadership, Communication, Problem-solving"
            }}
        }}

        Resume content:
        {content}
        """
    ).strip()


async def parse_pdf_resume(
    context: context.AnyContext, file_content: bytes
) -> parsed_resume_models.ParsedResume:
    """Parse PDF resume using GPT.

    Args:
        context: Application context
        file_content: PDF file content as bytes

    Returns:
        Structured parsed resume data

    Raises:
        ResumeParsingFailed: If parsing fails
    """
    try:
        text_content = _extract_text_from_pdf(file_content)

        logger.info(f"Extracted {len(text_content)} characters from PDF")

        # TODO: add to prompt message about finding at least year in dates
        user_prompt = _get_user_prompt(text_content)

        parsed_resume = await openai_client.parse_with_gpt(
            response_model=parsed_resume_models.ParsedResume,
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        logger.info(f"Successfully parsed resume for: {parsed_resume.name}")
        return parsed_resume

    except Exception as e:
        logger.exception(f"Resume parsing failed: {e}")
        raise ai_exceptions.ResumeParsingFailed from e


def _extract_text_from_pdf(file_content: bytes) -> str:
    try:
        import io

        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text_parts = []
        for page in pdf_reader.pages:
            text_parts.append(page.extract_text())

        full_text = "\n\n".join(text_parts)

        if not full_text.strip():
            raise ai_exceptions.ResumeParsingFailed

        return full_text

    except Exception as e:
        logger.exception(f"PDF text extraction failed: {e}")
        raise ai_exceptions.ResumeParsingFailed from e
