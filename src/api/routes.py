
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query, Response, status

from api.models import MessageCreate, MessageResponse, MessageRole, MessageUpdate
from api import storage


router = APIRouter(prefix="/api/v1/messages", tags=["Messages"])


def get_message_or_404(message_id: int) -> MessageResponse:
    message = storage.messages.get(message_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "message_not_found",
                "message": f"Message with ID {message_id} was not found.",
            },
        )

    return message


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a message",
)
def create_message(message: MessageCreate):
    message_id = storage.next_message_id

    new_message = MessageResponse(
        id=message_id,
        role=message.role,
        content=message.content,
        created_at=datetime.now(timezone.utc),
    )

    storage.messages[message_id] = new_message
    storage.next_message_id += 1

    return new_message


@router.get(
    "",
    response_model=list[MessageResponse],
    status_code=status.HTTP_200_OK,
    summary="List messages",
)
def list_messages(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    role: MessageRole | None = None,
):
    result = list(storage.messages.values())

    if role is not None:
        result = [message for message in result if message.role == role]

    return result[offset : offset + limit]


@router.get(
    "/{message_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a message",
)
def get_message(message_id: int):
    return get_message_or_404(message_id)


@router.patch(
    "/{message_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a message",
)
def update_message(message_id: int, update: MessageUpdate):
    message = get_message_or_404(message_id)

    updated_message = message.model_copy(
        update={"content": update.content}
    )

    storage.messages[message_id] = updated_message
    return updated_message


@router.delete(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a message",
)
def delete_message(message_id: int):
    get_message_or_404(message_id)
    del storage.messages[message_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
