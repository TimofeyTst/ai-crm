from ai_crm.internal.repository.postgresql.collect_response import (
    collect_response,
)
from ai_crm.pkg import context
from ai_crm.pkg.connectors.postgresql import psql
from ai_crm.pkg.models.ai_crm import resume as resume_models


@collect_response
async def create_resume(
    context: context.AnyContext,
    user_id: str,
    filename: str,
    original_filename: str,
    file_size: int,
    mime_type: str,
    storage_path: str,
    storage_type: str,
    title: str | None = None,
    description: str | None = None,
) -> resume_models.Resume:
    async with psql.get_connection(context) as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO resumes (
                user_id, filename, original_filename, file_size,
                mime_type, storage_path, storage_type, title, description
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING *
            """,
            user_id,
            filename,
            original_filename,
            file_size,
            mime_type,
            storage_path,
            storage_type,
            title,
            description,
        )
        return row


@collect_response
async def get_resume_by_id(
    context: context.AnyContext, resume_id: str
) -> resume_models.Resume:
    async with psql.get_connection(context, read_only=True) as conn:
        row = await conn.fetchrow(
            "SELECT * FROM resumes WHERE id = $1", resume_id
        )
        return row


@collect_response
async def get_user_resumes(
    context: context.AnyContext,
    user_id: str,
    only_active: bool = True,
) -> list[resume_models.Resume]:
    async with psql.get_connection(context, read_only=True) as conn:
        if only_active:
            rows = await conn.fetch(
                """
                SELECT * FROM resumes
                WHERE user_id = $1 AND is_active = TRUE
                ORDER BY created_at DESC
                """,
                user_id,
            )
        else:
            rows = await conn.fetch(
                """
                SELECT * FROM resumes
                WHERE user_id = $1
                ORDER BY created_at DESC
                """,
                user_id,
            )
        return rows


async def delete_resume(context: context.AnyContext, resume_id: str) -> bool:
    """Soft delete resume (set is_active to False).

    Returns:
        True if deleted successfully
    """
    async with psql.get_connection(context) as conn:
        result = await conn.execute(
            """
            UPDATE resumes
            SET is_active = FALSE, updated_at = NOW()
            WHERE id = $1
            """,
            resume_id,
        )
        return result == "UPDATE 1"
