from Node import Node
from Event import Event
from Message import Message
import Util

class Main:

    node_configuration_filePath = "Topology.txt"  # Specify the node configuration file path
    event_configuration_filePath = "events.txt"    # Specify the event configuration file path

    node_list = []        # List of all the active Nodes
    event_list = []       # List of all the events

    current_time = 0

    # Constructor of Main file
    def __init__(self):
        print("Main constructor")
        self.read_node_configuration_file(self.node_configuration_filePath)    # Read the node configuration file
        self.read_event_configuration_file(self.event_configuration_filePath)  # Read the event configuration file
        self.trigger_event()
        self.print_event_list()
        #self.print_nodes_connected_list()

    # print the active nodes
    def print_event_list(self):
        for node in self.node_list:
            print(node.node_Id)

    # print node's connected list
    def print_nodes_connected_list(self):
        for node in self.node_list:
            print("The present node id is " + node.node_Id)
            for key,val in node.connected_nodes.items():
                print("key: " + key + ":" + val)

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
            self.create_new_event(x.rstrip())

    # Create a new node and configure it's neighbours
    def create_new_node(self, node_info):
        #print node_info
        node_info_list = node_info.split(":")

        node_id = node_info_list[0]
        subscription_list = node_info_list[1].split(",")
        connected_node_list = node_info_list[2].split(",")
        connected_node_cost_list = node_info_list[3].split(",")

        new_node = Node(node_id, subscription_list, connected_node_list, connected_node_cost_list)
        self.node_list.append(new_node)                              # Add to the node list
        #new_node.connected_nodes.clear()

    # Delete the existing node and configure it's neighbours
    def remove_node(self, node_info):

        for node in self.node_list:
            if node_info in node.connected_nodes:
                node.connected_nodes.pop(node_info)

        for node in self.node_list:
            if node.node_Id == node_info:
                self.node_list.remove(node)

    # Create new event and add it to the event queue
    def create_new_event(self, event_info):
        print(event_info)
        event_info_list = event_info.split(":")
        timestamp = event_info_list[0]
        event_type = event_info_list[1]

        if event_type == 'ADD_NODE':
            print("The event type is Add Node")
            node_id = event_info_list[2]
            subscription_list = event_info_list[3].split(",")
            connected_node_list = event_info_list[4].split(",")
            connected_node_cost_list = event_info_list[5].split(",")
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
            subscription_list = event_info_list[3].split(",")
            new_Event = Event(timestamp, event_type, node_id, subscription_list, None, None, None, None)

        elif event_type == 'DELETE_SUBSCRIPTION':
            print("The event type is Delete Subscription")
            node_id = event_info_list[2]
            subscription_list = event_info_list[3].split(",")
            new_Event = Event(timestamp, event_type, node_id, subscription_list, None, None, None, None)

        self.event_list.append(new_Event)                          # Add to the event list

    # Trigger the event based on the time_stamp
    def trigger_event(self):
        while self.current_time < 1000000:
            self.current_time += 1
            if len(self.event_list) > 0:
                event = self.event_list[0]
                if self.current_time == int(event.time_stamp):
                    event = self.event_list.pop(0)
                    if event.event_type == 'ADD_NODE':
                        print("Trigger event:"+ event.event_type)
                        node_info = event.node_id + ":" + self.get_string_from_list(event.subscription_list) + ":" + self.get_string_from_list(event.connected_node_list) + ":" + self.get_string_from_list(event.connected_node_cost_list)
                        self.add_new_node(node_info)
                        logger_message = str(self.current_time) + ":" + "ANODE" + ":" + event.node_id + ":" + self.get_string_from_list(event.connected_node_list) + ":" + self.get_string_from_list(event.connected_node_cost_list) + "\n"
                        Util.log_file.write(logger_message)

                    elif event.event_type == 'DELETE_NODE':
                        print("Trigger event:" + event.event_type)
                        node_info = event.node_id
                        self.remove_node(node_info)
                        logger_message = str(self.current_time) + ":" + "RNODE" + ":" + event.node_id  + "\n"
                        Util.log_file.write(logger_message)

                    elif event.event_type == 'SEND_MESSAGE':
                        # print("Trigger event:" + event.event_type)
                        node_id = event.node_id
                        new_list = self.node_list.copy()
                        for node in new_list:
                            if node.node_Id == node_id:
                                message_object = Message(event.message_topic, event.message, node.time_stamp,
                                                         node.time_stamp, Util.MESSAGE_TIMER)
                                node.send_message(message_object, self.current_time)
                                break

                    elif event.event_type == 'RECEIVE_MESSAGE':
                        print("Trigger event:" + event.event_type)
                        node_id = event.node_id
                        for node in self.node_list:
                            if node.node_Id == node_id:
                                node.receive_message()
                                break

                    elif event.event_type == 'ADD_SUBSCRIPTION':
                        print("Trigger event:" + event.event_type)
                        self.add_new_subscription(event)

                    elif event.event_type == 'DELETE_SUBSCRIPTION':
                        print("Trigger event:" + event.event_type)
                        self.delete_subscription(event)

            self.update_message_queue()
            self.update_incoming_message_queue()

    # Concatenate each item in the list to form a string
    def get_string_from_list(self, list):
        ans = ""
        for item in list:
            ans += item
            ans += ','
        return ans[0:len(ans)-1]

    # Dynamically add new nodes based on the event
    def add_new_node(selfs, node_info):
        selfs.create_new_node(node_info)
        new_node = selfs.node_list[len(selfs.node_list)-1]

        for nodeId in new_node.connected_nodes:
            for node in selfs.node_list:
                if node.node_Id == nodeId:
                    cost = new_node.connected_nodes[str(nodeId)]
                    node.connected_nodes[str(new_node.node_Id)] = cost

    # Dynamically add new subscription to the node
    def add_new_subscription(selfs, event):
        curr_node = event.node_id
        for node in selfs.node_list:
            if node.node_Id == curr_node:
                curr_subscription_list = node.subscription_list
                for item in event.subscription_list:
                    curr_subscription_list.append(item.rstrip())
                print(node.subscription_list)

    # Dynamically remove subscription from the node
    def delete_subscription(selfs, event):
        curr_Node = event.node_id
        for node in selfs.node_list:
            if node.node_Id == curr_Node:
                curr_subscription_list = node.subscription_list
                for item in event.subscription_list:
                    curr_subscription_list.remove(item)
                print(node.subscription_list)

    # Update the outgoing queue for every clock tick
    def update_incoming_message_queue(self):

        for node in self.node_list:
            i = 0
            while i < len(node.incoming_message_queue):
                i += 1
                message_object = node.incoming_message_queue.pop(0)

                logger_message = str(self.current_time) + ":" + "RECV" + ":" + node.node_Id + ":" + message_object.topic + ":" + message_object.msg + ":"

                is_subscribed = "NO"
                for topic in node.subscription_list:
                    if topic in message_object.topic:
                        is_subscribed = "YES"
                        node.time_stamp = max (int(node.time_stamp), int(message_object.node_time_stamp)) + 1
                        print(message_object.msg + " is consumed by node " + node.node_Id + " at " + str(self.current_time))
                        break

                logger_message += is_subscribed.rstrip() + ":" + str(node.time_stamp) +"\n"
                Util.log_file.write(logger_message)

                message_object.time_to_live -= 1
                if message_object.time_to_live > 0:
                    node.send_message(message_object, self.current_time)

    # Update the outgoing queue for every clock tick
    def update_message_queue(self):

        for node in self.node_list:
            i = 0
            while i < len(node.out_going_queue_time):
                if node.out_going_queue_time[i] == self.current_time:
                    for receiving_node in self.node_list:
                        logger_message = str(self.current_time) + ":" + "ARIV" + ":" + node.node_Id + ":"
                        if i < len(node.random_nodes_selected) and receiving_node.node_Id == node.random_nodes_selected[i]:
                            logger_message += receiving_node.node_Id + "\n"
                            message = node.out_going_message_queue[i]
                            receiving_node.incoming_message_queue.append(message)

                            node.out_going_message_queue.pop(i)
                            node.out_going_queue_time.pop(i)
                            node.random_nodes_selected.pop(i)

                            print(receiving_node.node_Id + " updated")
                            Util.log_file.write(logger_message)
                            i = 0
                i += 1

    # Get the node with specific node Id
    def get_node(self, node_id):
        for node in self.node_list:
            if node.node_Id == node_id:
                return node

# Instantiate an object of Main
mainObj = Main()


