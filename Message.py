class Message:
    def __init__(self, topic, msg, node_time_stamp, intiated_time, time_to_live):
        self.topic = topic
        self.msg = msg
        self.node_time_stamp = node_time_stamp
        self.intiated_time = intiated_time
        self.time_to_live = time_to_live


