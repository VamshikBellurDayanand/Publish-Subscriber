from Util import EventType

class Event:
    time_stamp = 0
    event_type = 0
    send_node = 0

    def __init__(self, time_stamp, event_type, send_node):
        self.time_stamp = time_stamp
        self.event_type = event_type
        self.send_node = send_node