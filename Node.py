import random
import Util
import time
import Message
class Node:

    # Node id which identifies each node
    node_Id = 0

    # Dictionary to hold the connected nodes as keys and connection cost as values
    connected_nodes = {}

    # List to hold the link cost for sending the messages.
    out_going_queue_time = list()

    # List to hold the incoming message queue
    incoming_message_queue = list()

    # List to hold the outgoing message queue
    out_going_message_queue = list()

    # List of random nodes selected
    random_nodes_selected = list()

    # List of random nodes to receive the message
    random_nodes_selected_to_recieve = list()

    # No of random nodes, the message to be gossiped.
    no_of_random_nodes = Util.NO_OF_RANDOM_NODES

    # Timestamp of each node
    time_stamp = 0

    # Subscription List
    subscription_list = set()

    # Constructor of Node
    def __init__(self, node_Id, subscription_list, connected_node_list, connected_node_cost_list):
        self.incoming_message_queue = list()
        self.out_going_queue_time = list()
        self.out_going_message_queue = list()
        self.random_nodes_selected = list()
        self.random_nodes_selected_to_recieve = list()
        self.connected_nodes = {}
        self.node_Id = node_Id
        self.subscription_list = subscription_list
        self.time_stamp = 0

        i = 0
        while i < len(connected_node_list):
            self.connected_nodes[str(connected_node_list[i])] = connected_node_cost_list[i].rstrip()
            i += 1

    # Nodes execute this method to get the message
    def get_message(self):
        print ("Get message called")

    # Handle each message present in the incoming queue
    def process_message_from_incoming_queue(self):
        print ("Process message called")

    # Send message to other nodes by placing the message in the outgoing queue
    def send_message(self, message_object, global_time):
        #print ("Send message called")
        put_message = message_object
        list_of_chosen_nodes = random.sample(set(self.connected_nodes),self.no_of_random_nodes)  # select random nodes to gossip
        put_message.node_time_stamp = self.time_stamp + 1

        for node in list_of_chosen_nodes:
            self.random_nodes_selected.append(node)
            self.out_going_message_queue.append(put_message)
            self.out_going_queue_time.append(int(self.connected_nodes[node]) + global_time)
            print(str(global_time) + ":" + "SENT" + ":" + self.node_Id + ":" + node + ":" + message_object.topic + ":" + message_object.msg + ":" + str(int(self.connected_nodes[node]) + global_time) + "\n")
            Util.log_file.write(str(global_time) + ":" + "SENT" + ":" + self.node_Id + ":" + node + ":" + message_object.topic + ":" + message_object.msg + ":" + str(int(self.connected_nodes[node]) + global_time) + "\n")
            #print("Node selected is " + node + " and the time it should send message is " + str(int(self.connected_nodes[node]) + global_time))

    # The message is currently in the randomly chosen node's incoming queue
    def pull_gossip(self):
        print("pull gossip called")
        list_of_chosen_nodes = random.sample(set(self.connected_nodes),self.no_of_random_nodes)  # select random nodes to gossip
        for node in list_of_chosen_nodes:
            self.random_nodes_selected_to_recieve.append(node)

    def get_random_choosen_nodes(self):
        list_of_chosen_nodes = random.sample(set(self.connected_nodes), self.no_of_random_nodes)
        return list_of_chosen_nodes


    def set_out_going_message_queue(self, out_going_message_queue):
        self.out_going_message_queue = out_going_message_queue

    def get_out_going_message_queue(self):
        return self.out_going_message_queue



