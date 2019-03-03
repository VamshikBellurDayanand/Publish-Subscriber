from Node import Node

class Main:

    node_configuration_filePath = "C:/Users/Vamshik B D/Desktop/VmWare.txt"  # Specify the node configuration file path
    event_configuration_filePath = "SOME_RANDOM_EVENT_CONFIGURATION_PATH"    # Specify the event configuration file path

    node_list = []        # List of all the active Nodes
    event_list = []       # List of all the events

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
            print x
        self.create_new_node(x)

    # Read the event configuration file and trigger the respective events
    def read_event_configuration_file(self, filePath):

        file_object = open(filePath, "r")

        # printing the data from file : line by line
        for x in file_object:
            print x

    # Create a new node and configure it's neighbours
    def create_new_node(self, node_info):
        print node_info
        newnode = Node(1)
        print newnode.node_Id

    # Delete the existing node and configure it's neighbours
    def remove_node(self, node_info):
        print node_info


# Instantiate an object of Main
mainObj = Main()


