from Node import Node
from Event import Event

class Main:

    node_configuration_filePath = "Topology.txt"  # Specify the node configuration file path
    event_configuration_filePath = "events.txt"    # Specify the event configuration file path

    node_list = []        # List of all the active Nodes
    event_list = []       # List of all the events

    current_time = 0

    # Constructor of Main file
    def __init__(self):
        print ("Main constructor")
        self.read_node_configuration_file(self.node_configuration_filePath)    # Read the node configuration file
        self.read_event_configuration_file(self.event_configuration_filePath)  # Read the event configuration file

    # Read the Node configuration file and create the Node objects
    def read_node_configuration_file(self, filePath):

        file_object = open(filePath, "r")

        # printing the data from file : line by line
        for x in file_object:
            self.create_new_node(x)

    # Read the event configuration file and trigger the respective events
    def read_event_configuration_file(self, filePath):

        file_object = open(filePath, "r")

        # printing the data from file : line by line
        for x in file_object:
            self.create_new_event(x)

    # Create a new node and configure it's neighbours
    def create_new_node(self, node_info):
        #print node_info
        node_info_list = node_info.split(":")

        node_id = node_info_list[0]
        subscription_list = node_info_list[1].split(",")
        connected_node_list = node_info_list[2].split(",")
        connected_node_cost_list = node_info_list[3].split(",")

        new_node = Node(node_id, subscription_list, connected_node_list, connected_node_cost_list)
        print(new_node.node_Id)
        print(new_node.connected_nodes)
        self.node_list.append(new_node)                              # Add to the node list
        new_node.connected_nodes.clear()

    # Delete the existing node and configure it's neighbours
    def remove_node(self, node_info):
        print(node_info)
        if node_info in self.node_list:                             # If node is active and is not deleted
            for node in node_info.connected_nodes:                  # Update in all of the node's neighbours
                if node_info.node_Id in node.connected_nodes:
                    node.connected_nodes.pop(node_info.node_Id)
            self.node_list.remove(node_info.node_Id)                # Remove the node from the list
        else:
            print("Node with id " + node_info.node_Id + " is already deleted.")

    # Create new event and add it to the event queue
    def create_new_event(self, event_info):
        print(event_info)
        event_info_list = event_info.split(":")
        timestamp = event_info_list[0]
        event_type = event_info_list[1]

        if event_type == 'ADD_NODE':
            print("The event type is Add Node")
            node_id = event_info_list[2]
            print(node_id)
            subscription_list = event_info_list[3].split(",")
            print(subscription_list)
            connected_node_list = event_info_list[4].split(",")
            print(connected_node_list)
            connected_node_cost_list = event_info_list[5].split(",")
            print(connected_node_cost_list)

            new_Event = Event(timestamp, event_type, node_id, subscription_list, connected_node_list, connected_node_cost_list, None, None)

        elif event_type == 'DELETE_NODE':
            print("The event type is Delete Node")
            node_id = event_info_list[2]

            new_Event = Event(timestamp, event_type, node_id, None, None, None, None, None)

        elif event_type == 'SEND_MESSAGE':
            print("The event type is Send Message")
            node_id = event_info_list[2]
            message = event_info_list[3]
            message_topic = event_info_list[4]

            new_Event = Event(timestamp, event_type, node_id, None, None, None, message, message_topic)

        elif event_type == 'RECEIVE_MESSAGE':
            print("The event type is Receive Message")
            node_id = event_info_list[2]

            new_Event = Event(timestamp, event_type, node_id, None, None, None, None, None)

        elif event_type == 'ADD_SUBSCRIPTION':
            print("The event type is Add Subscription")
            node_id = event_info_list[2]
            subscription_list = event_info_list[3]

            new_Event = Event(timestamp, event_type, node_id, subscription_list, None, None, None, None)

        elif event_type == 'DELETE_SUBSCRIPTION':
            print("The event type is Delete Subscription")
            node_id = event_info_list[2]
            subscription_list = event_info_list[3]

            new_Event = Event(timestamp, event_type, node_id, subscription_list, None, None, None, None)

        self.event_list.append(event_info)                          # Add to the event list


    # Trigger the event based on the time_stamp
    def trigger_event(self):
        print("Trigger event called")

    # Dynamically add new nodes based on the event
    def add_new_node(selfs, node_info):
        print(node_info)

        selfs.create_new_node(node_info)

# Instantiate an object of Main
mainObj = Main()


