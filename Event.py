from Util import EventType

class Event:
    time_stamp = 0
    event_type = 0
    node_id = 0
    subscription_list = set()
    connected_node_list = []
    connected_node_cost_list = []
    message = ''
    message_topic = ''

    # Event Constructor for Add Node
    def __init__(self, time_stamp, event_type, node_id, subscription_list, connected_node_list, connected_node_cost_list, message, message_topic):
        self.time_stamp = time_stamp
        self.event_type = event_type
        self.node_id = node_id
        self.subscription_list = subscription_list
        self.connected_node_list = connected_node_list
        self.connected_node_cost_list = connected_node_cost_list
        self.message = message
        self.message_topic = message_topic

