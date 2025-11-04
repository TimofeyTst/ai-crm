"""OpenAI GPT client for AI operations."""

from typing import TypeVar

from pydantic import BaseModel

from ai_crm.pkg.configuration import settings
from ai_crm.pkg.logger import logger as logger_lib
from ai_crm.pkg.models.exceptions import ai as ai_exceptions
from openai import AsyncOpenAI

logger = logger_lib.get_logger(__name__)

T = TypeVar("T", bound=BaseModel)


def get_openai_client() -> AsyncOpenAI:
    """Get configured OpenAI client."""
    return AsyncOpenAI(
        api_key=settings.ai_crm_env.API.OPENAI_API_KEY.get_secret_value()
    )


async def parse_with_gpt(
    response_model: type[T],
    system_prompt: str,
    user_prompt: str,
) -> T:
    """Parse content using GPT with structured output (json_schema).

    Args:
        response_model: Pydantic model for response structure
        system_prompt: System prompt for GPT
        user_prompt: User prompt with content

    Returns:
        Parsed structured data

    Raises:
        OpenAIAPIError: If API call fails
    """
    client = get_openai_client()

    try:
        logger.info(
            f"Sending parsing request to OpenAI with model "
            f"{settings.ai_crm_env.API.OPENAI_MODEL}"
        )

        response = await client.beta.chat.completions.parse(
            model=settings.ai_crm_env.API.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=settings.ai_crm_env.API.OPENAI_MAX_TOKENS,
            temperature=settings.ai_crm_env.API.OPENAI_TEMPERATURE,
            response_format=response_model,
        )

        parsed_message = response.choices[0].message
        if not parsed_message.parsed:
            logger.error(f"Failed to parse response: {parsed_message.refusal}")
            raise ai_exceptions.ResumeParsingFailed

        logger.info("Successfully parsed content with GPT")
        return parsed_message.parsed

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise ai_exceptions.OpenAIAPIError from e


async def personalize_with_gpt(
    response_model: type[T],
    system_prompt: str,
    user_prompt: str,
) -> T:
    """Personalize resume using GPT with structured output (json_schema).

    Args:
        response_model: Pydantic model for response structure
        system_prompt: System prompt for personalization
        user_prompt: User prompt with resume data and job description

    Returns:
        Personalized resume data

    Raises:
        OpenAIAPIError: If API call fails
    """
    client = get_openai_client()

    try:
        logger.info("Sending personalization request to OpenAI")

        response = await client.beta.chat.completions.parse(
            model=settings.ai_crm_env.API.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=settings.ai_crm_env.API.OPENAI_MAX_TOKENS,
            temperature=settings.ai_crm_env.API.OPENAI_TEMPERATURE,
            response_format=response_model,
        )

        parsed_message = response.choices[0].message
        if not parsed_message.parsed:
            logger.error(f"Failed to parse response: {parsed_message.refusal}")
            raise ai_exceptions.ResumePersonalizationFailed

        logger.info("Successfully personalized resume with GPT")
        return parsed_message.parsed

    except Exception as e:
        logger.error(f"OpenAI personalization error: {e}")
        raise ai_exceptions.OpenAIAPIError from e
