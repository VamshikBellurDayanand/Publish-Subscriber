import enum

NO_OF_RANDOM_NODES = 3   # No of random nodes, message to be gossipped
log_file = open("logger.txt", "a")
MESSAGE_TIMER = 5

class EventType(enum.Enum):
    ADD_NODE = 1
    DELETE_NODE = 2
    SEND_MESSAGE = 3
    RECEIVE_MESSAGE = 4
    ADD_SUBSCRIPTION = 5
    DELETE_SUBSCRIPTION = 6