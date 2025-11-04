"""AI-powered resume parsing service using GPT."""

import PyPDF2

from ai_crm.pkg import context
from ai_crm.pkg.connectors import openai as openai_connector
from ai_crm.pkg.logger import logger as logger_lib
from ai_crm.pkg.models.ai_crm import parsed_resume as parsed_resume_models
from ai_crm.pkg.models.exceptions import ai as ai_exceptions

logger = logger_lib.get_logger(__name__)

SYSTEM_PROMPT = """You are an expert resume parser.
Extract structured information from resumes accurately.
Return data in valid JSON format matching the schema provided.
For dates, use ISO format (YYYY-MM-DD).
If information is not available, use null."""

USER_PROMPT = """Parse the following resume and extract all relevant information.
Return the data in JSON format with these fields:
- name: Full name
- position: Desired or current position
- email: Email address
- linkedin: LinkedIn profile URL
- phone: Phone number
- summary: Professional summary
- education: List of education entries with institution, degree, from_date, to_date, description
- professional_experience: List of work experiences with company_name, position, hired_date, fired_date, achievements
- certifications: List of certifications with name, description, date_obtained
- skills: Object with tech_stack, languages, soft_skills

Resume content:
{content}
"""


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

        parsed_resume = await openai_connector.parse_with_gpt(
            content=text_content,
            response_model=parsed_resume_models.ParsedResume,
            system_prompt=SYSTEM_PROMPT,
            user_prompt=USER_PROMPT,
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
