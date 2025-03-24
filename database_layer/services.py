import logging
from typing import Sequence, TypeVar, Type, Generic

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .core import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseService(Generic[ModelType]):
    model: Type[ModelType] = NotImplementedError
    logger = logging.getLogger(f"{__name__}:{model}")

    @classmethod
    async def add(
            cls,
            session: AsyncSession,
            data: ModelType | list[ModelType],
            on_conflict_elements: list[str] = None
    ) -> Sequence[ModelType]:
        if on_conflict_elements is None:
            on_conflict_elements = ['id']
        if isinstance(data, list):
            stmt = insert(cls.model).values([i.to_add_schema().model_dump() for i in data])
        else:
            stmt = insert(cls.model).values(data.to_add_schema().model_dump())

        stmt = stmt.on_conflict_do_nothing(index_elements=on_conflict_elements).returning(cls.model)
        res = await session.execute(stmt)
        await session.commit()
        result = res.scalars().all()
        cls.logger.debug(result)
        return result

    @classmethod
    async def get(
            cls,
            session: AsyncSession,
            offset: int = 0,
            limit: int = 1,
            filter_by: dict = None
    ) -> Sequence[ModelType]:
        if filter_by is None:
            filter_by = {}
        result = (await session.execute(select(cls.model).
                                        filter_by(**filter_by).
                                        offset(offset).
                                        limit(limit))
                  ).scalars().all()
        cls.logger.debug(result)
        return result

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            instance: ModelType
    ) -> ModelType:
        await session.merge(instance)
        await session.commit()
        cls.logger.debug(instance)
        return instance

    # TODO: delete method.
