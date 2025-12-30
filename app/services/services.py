from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import crud
from app.crud.registry import get_model, get_id_field
from app.core.exceptions import logic_exception
from app.core.error_codes import ErrorCodes


async def get_entity(db: AsyncSession, name: str, id_value: Any) -> Any:
    """Get an entity by ID, raising exception if not found."""
    model = get_model(name)
    id_field = get_id_field(name)
    
    instance = await crud.get_by_id(db, model, id_field, id_value)
    if not instance:
        raise logic_exception(
            code=ErrorCodes.not_found,
            message=f"{name.capitalize()} not found",
            status_code=404
        )
    return instance


async def list_entity(
    db: AsyncSession,
    name: str,
    skip: int = 0,
    limit: int = 100
) -> list[Any]:
    """List all entities with pagination."""
    model = get_model(name)
    return await crud.get_all(db, model, skip=skip, limit=limit)


async def create_entity(
    db: AsyncSession,
    name: str,
    data: dict[str, Any],
    actor_name: str
) -> Any:
    """Create an entity with validation."""
    model = get_model(name)
    
    # User: unique user_email validation
    if name == "user" and "user_email" in data:
        existing = await crud.get_by_field(db, model, "user_email", data["user_email"])
        if existing:
            raise logic_exception(
                code=ErrorCodes.user_exists,
                message="User Already Exists"
            )
    
    # Student: unique user_id validation
    if name == "student" and "user_id" in data:
        existing = await crud.get_by_field(db, model, "user_id", data["user_id"])
        if existing:
            raise logic_exception(
                code=ErrorCodes.user_exists,
                message="Student already exists for this user"
            )
    
    # Advisor: unique user_id validation
    if name == "advisor" and "user_id" in data:
        existing = await crud.get_by_field(db, model, "user_id", data["user_id"])
        if existing:
            raise logic_exception(
                code=ErrorCodes.user_exists,
                message="Advisor already exists for this user"
            )
    
    # Jury: unique user_id validation
    if name == "jury" and "user_id" in data:
        existing = await crud.get_by_field(db, model, "user_id", data["user_id"])
        if existing:
            raise logic_exception(
                code=ErrorCodes.user_exists,
                message="Jury already exists for this user"
            )
    
    return await crud.create(db, model, data, actor_name)


async def update_entity(
    db: AsyncSession,
    name: str,
    id_value: Any,
    data: dict[str, Any],
    actor_name: str
) -> Any:
    """Update an entity, raising exception if not found."""
    model = get_model(name)
    id_field = get_id_field(name)
    
    instance = await crud.update(db, model, id_field, id_value, data, actor_name)
    if not instance:
        raise logic_exception(
            code=ErrorCodes.not_found,
            message=f"{name.capitalize()} not found",
            status_code=404
        )
    return instance


async def delete_entity(db: AsyncSession, name: str, id_value: Any) -> bool:
    """Delete an entity, raising exception if not found."""
    model = get_model(name)
    id_field = get_id_field(name)
    
    success = await crud.delete(db, model, id_field, id_value)
    if not success:
        raise logic_exception(
            code=ErrorCodes.not_found,
            message=f"{name.capitalize()} not found",
            status_code=404
        )
    return True

