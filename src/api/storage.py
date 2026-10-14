
from api.models import MessageResponse


messages: dict[int, MessageResponse] = {}
next_message_id = 1
