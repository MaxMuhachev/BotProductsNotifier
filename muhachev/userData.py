# Здесь хранятся пользовательские данные.
# Т.к. это словарь в памяти, то при перезапуске он очистится
class User:
    user_data = {}


class UserKeys:
    SCORE = "score"
    SECTION = "section"
    LAST_RESULT = "last_result"
    SCORE_MESS_ID = "score_message_id"
    CAN_HALF = "can_half"
    CAN_ERROR = "can_error"
