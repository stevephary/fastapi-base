from typing import List, TypeVar, Generic
from math import ceil
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class Pagination(GenericModel, Generic[T]):
    page: int
    size: int
    total: int
    pages: int
    results: List[T]

    @classmethod
    def create(cls, data: List[T], total: int, page: int = 1, size: int = 10) -> "Pagination[T]":
        pages = ceil(total / size) if size else 0
        return cls(
            page=page,
            size=size,
            total=total,
            pages=pages,
            results=data,
        )


class Paginator:
    def __init__(self, page: int = 1, size: int = 10):
        self.page = max(page, 1)
        self.size = max(size, 1)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size

    def slice(self, items: List[T]) -> List[T]:
        start = self.offset
        end = start + self.size
        return items[start:end]
