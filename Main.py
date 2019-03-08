from Node import Node

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
            #print x
            self.create_new_node(x)

    # Read the event configuration file and trigger the respective events
    def read_event_configuration_file(self, filePath):

        file_object = open(filePath, "r")

        # printing the data from file : line by line
        for x in file_object:
            #print x
            self.create_new_event(x)

    # Create a new node and configure it's neighbours
    def create_new_node(self, node_info):
        #print node_info
        node_info_list = node_info.split(":")

        node_id = node_info_list[0]
        subscription_list = node_info_list[1]
        connected_node_list = node_info_list[2].split(",")
        connected_node_cost_list = node_info_list[3].split(",")
        timestamp = node_info_list[4]

        new_node = Node(node_id, subscription_list, connected_node_list, connected_node_cost_list, timestamp)
        print new_node.node_Id
        print new_node.connected_nodes
        self.node_list.append(new_node)                              # Add to the node list

    # Delete the existing node and configure it's neighbours
    def remove_node(self, node_info):
        print node_info
        if node_info in self.node_list:                             # If node is active and is not deleted
            for node in node_info.connected_nodes:                  # Update in all of the node's neighbours
                if node_info.node_Id in node.connected_nodes:
                    node.connected_nodes.pop(node_info.node_Id)
            self.node_list.remove(node_info.node_Id)                # Remove the node from the list
        else:
            print ("Node with id " + node_info.node_Id + " is already deleted.")

    # Create new event and add it to the event queue
    def create_new_event(self, event_info):
        print event_info
        self.event_list.append(event_info)                          # Add to the event list
        self.event_list.sort(key=lambda x: x.time_stamp)

    # Trigger the event based on the time_stamp
    def trigger_event(self):
        print ("Trigger event called")

    # Dynamically add new nodes based on the event
    def add_new_node(selfs, node_info):
        print (node_info)

        selfs.create_new_node(node_info)

# Instantiate an object of Main
mainObj = Main()


