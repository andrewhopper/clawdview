"""Example items router demonstrating CRUD patterns with OpenAPI annotations."""

from datetime import datetime
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse

from ..logging_config import get_logger
from ..models import ItemCreate, ItemResponse, PaginatedResponse

router = APIRouter(
    prefix="/items",
    tags=["Items"],
    responses={
        404: {"description": "Item not found"},
        500: {"description": "Internal server error"},
    },
)

# In-memory store for example (replace with database)
_items: dict[str, ItemResponse] = {}


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
    description="Creates a new item with the provided name and optional description.",
    responses={
        201: {"description": "Item created successfully"},
        422: {"description": "Validation error"},
    },
)
async def create_item(item: ItemCreate) -> ItemResponse:
    """Create a new item."""
    log = get_logger("items.create")

    item_id = str(uuid4())[:8]
    now = datetime.utcnow()

    response = ItemResponse(
        id=item_id,
        name=item.name,
        description=item.description,
        created_at=now,
        updated_at=now,
    )
    _items[item_id] = response

    log.info("Item created", item_id=item_id)
    return response


@router.get(
    "",
    response_model=PaginatedResponse[ItemResponse],
    summary="List all items",
    description="Returns a paginated list of all items.",
)
async def list_items(
    page: Annotated[int, Query(ge=1, description="Page number (1-indexed)")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10,
) -> PaginatedResponse[ItemResponse]:
    """List all items with pagination."""
    items = list(_items.values())
    total = len(items)

    start = (page - 1) * page_size
    end = start + page_size
    page_items = items[start:end]

    return PaginatedResponse(
        items=page_items,
        total=total,
        page=page,
        page_size=page_size,
        has_next=end < total,
    )


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get an item by ID",
    description="Returns a single item by its unique identifier.",
)
async def get_item(item_id: str) -> ItemResponse:
    """Get an item by ID."""
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    return _items[item_id]


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
    description="Permanently deletes an item by its unique identifier.",
    responses={
        204: {"description": "Item deleted successfully"},
        404: {"description": "Item not found"},
    },
)
async def delete_item(item_id: str) -> None:
    """Delete an item."""
    log = get_logger("items.delete")

    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")

    del _items[item_id]
    log.info("Item deleted", item_id=item_id)
