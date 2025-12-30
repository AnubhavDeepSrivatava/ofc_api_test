from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase


async def create(
    db: AsyncSession,
    model: type[DeclarativeBase],
    data: dict[str, Any],
    actor_name: Optional[str] = None
):
    """Create a new record with audit fields."""
    instance = model(**data)
    
    # Set audit fields only if they exist on the model
    if hasattr(instance, "created_by") and actor_name:
        instance.created_by = actor_name
    if hasattr(instance, "updated_by"):
        instance.updated_by = None
    
    db.add(instance)
    await db.commit()
    await db.refresh(instance)
    return instance


async def get_by_id(
    db: AsyncSession,
    model: type[DeclarativeBase],
    id_field: str,
    id_value: Any
) -> Optional[Any]:
    """Get a record by its primary key."""
    id_column = getattr(model, id_field)
    result = await db.execute(select(model).where(id_column == id_value))
    return result.scalar_one_or_none()


async def get_all(
    db: AsyncSession,
    model: type[DeclarativeBase],
    skip: int = 0,
    limit: int = 100
) -> list[Any]:
    """Get all records with pagination."""
    result = await db.execute(select(model).offset(skip).limit(limit))
    return list(result.scalars().all())


async def get_by_field(
    db: AsyncSession,
    model: type[DeclarativeBase],
    field_name: str,
    value: Any
) -> Optional[Any]:
    """Get a record by any field."""
    field = getattr(model, field_name)
    result = await db.execute(select(model).where(field == value))
    return result.scalar_one_or_none()


async def update(
    db: AsyncSession,
    model: type[DeclarativeBase],
    id_field: str,
    id_value: Any,
    data: dict[str, Any],
    actor_name: Optional[str] = None
) -> Optional[Any]:
    """Update a record partially with audit fields."""
    instance = await get_by_id(db, model, id_field, id_value)
    if not instance:
        return None
    
    # Update fields
    for key, value in data.items():
        if value is not None and hasattr(instance, key):
            setattr(instance, key, value)
    
    # Set audit field only if it exists
    if hasattr(instance, "updated_by") and actor_name:
        instance.updated_by = actor_name
    
    await db.commit()
    await db.refresh(instance)
    return instance


async def delete(
    db: AsyncSession,
    model: type[DeclarativeBase],
    id_field: str,
    id_value: Any
) -> bool:
    """Delete a record by its primary key."""
    instance = await get_by_id(db, model, id_field, id_value)
    if not instance:
        return False
    
    await db.delete(instance)
    await db.commit()
    return True

