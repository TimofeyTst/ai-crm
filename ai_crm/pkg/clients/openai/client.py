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

    model = settings.ai_crm_env.API.OPENAI_MODEL
    max_tokens = settings.ai_crm_env.API.OPENAI_MAX_TOKENS
    temperature = settings.ai_crm_env.API.OPENAI_TEMPERATURE

    logger.info(
        f"OpenAI Request [parse_with_gpt]: "
        f"model={model}, "
        f"max_tokens={max_tokens}, "
        f"temperature={temperature}, "
        f"response_format={response_model.__name__}"
    )
    logger.debug(f"System prompt: {system_prompt[:200]}...")
    logger.debug(
        f"User prompt length: {len(user_prompt)} chars, "
        f"preview: {user_prompt[:200]}..."
    )

    try:
        response = await client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            response_format=response_model,
        )

        parsed_message = response.choices[0].message
        usage = response.usage

        if usage:
            logger.info(
                f"OpenAI Response [parse_with_gpt]: "
                f"prompt_tokens={usage.prompt_tokens}, "
                f"completion_tokens={usage.completion_tokens}, "
                f"total_tokens={usage.total_tokens}"
            )

        if not parsed_message.parsed:
            logger.error(f"OpenAI parsing failed: {parsed_message.refusal}")
            raise ai_exceptions.ResumeParsingFailed

        logger.info(
            f"Successfully parsed content with GPT, "
            f"finish_reason={response.choices[0].finish_reason}"
        )
        return parsed_message.parsed

    except ai_exceptions.BaseAPIException:
        raise
    except Exception as e:
        logger.exception(
            f"OpenAI API error in parse_with_gpt: {type(e).__name__}: {e}"
        )
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

    model = settings.ai_crm_env.API.OPENAI_MODEL
    max_tokens = settings.ai_crm_env.API.OPENAI_MAX_TOKENS
    temperature = settings.ai_crm_env.API.OPENAI_TEMPERATURE

    logger.info(
        f"OpenAI Request [personalize_with_gpt]: "
        f"model={model}, "
        f"max_tokens={max_tokens}, "
        f"temperature={temperature}, "
        f"response_format={response_model.__name__}"
    )
    logger.debug(f"System prompt: {system_prompt[:200]}...")
    logger.debug(
        f"User prompt length: {len(user_prompt)} chars, "
        f"preview: {user_prompt[:200]}..."
    )

    try:
        response = await client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            response_format=response_model,
        )

        parsed_message = response.choices[0].message
        usage = response.usage

        if usage:
            logger.info(
                f"OpenAI Response [personalize_with_gpt]: "
                f"prompt_tokens={usage.prompt_tokens}, "
                f"completion_tokens={usage.completion_tokens}, "
                f"total_tokens={usage.total_tokens}"
            )

        if not parsed_message.parsed:
            logger.error(
                f"OpenAI personalization failed: {parsed_message.refusal}. Parsed message: {parsed_message}"
            )
            raise ai_exceptions.ResumePersonalizationFailed

        logger.info(
            f"Successfully personalized resume with GPT, "
            f"finish_reason={response.choices[0].finish_reason}"
        )
        return parsed_message.parsed

    except Exception as e:
        logger.exception(
            f"OpenAI API error in personalize_with_gpt: "
            f"{type(e).__name__}: {e}"
        )
        raise ai_exceptions.OpenAIAPIError from e
