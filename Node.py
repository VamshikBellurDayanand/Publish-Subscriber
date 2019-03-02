import Message

class Node:

    # Node id which identifies each node
    node_Id  = 0

    # Dictionary to hold the connected nodes as keys and connection cost as values
    connected_nodes = {}

    # List to hold the link cost for sending the messages.
    out_going_queue_time = []

    # List to hold the incoming message queue
    incoming_message_queue = []

    # List to hold the outgoing message queue
    out_going_message_queue = []


    # Constructor of Node
    def __init__(self):
        print ("This is Node's constructor")

    # Nodes execute this method to get the message
    def get_message_from_outgoing_queue(self):
        print ("Get message called")

    # Handle each message present in the incoming queue
    def process_message_from_incoming_queue(self):
        print ("Process message called")

    # Send message to other nodes by placing the message in the outgoing queue
    def send_message(self):
        print ("Send message called")







