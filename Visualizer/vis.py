import networkx as nx
import os
import sys
import matplotlib as mpl
mpl.use('Qt4Agg')
import matplotlib.pyplot as plt
import matplotlib.rcsetup as rcsetup
from matplotlib.pyplot import pause
import pylab
import random
import time
pylab.ion()

REFRESH_NODES = False
CYCLE_PERIOD=1.0
MAX_CYCLES=50

lines = []
colors = {} #dict of 'topic-msg':color
exe_script = [] #tuple format: <time, func, args...
pos = {}
rf_q = []

G = nx.Graph()

def load_topo(topo_file):
    try:
        f = open(topo_file, "r")
    except IOError:
        print ("Failed to open %s" % topo_file)
        return -1

    line = f.readline()
    while (line != ""):
        line = line.strip("\r\n")
        fields = line.split(":") 
        lines.append(fields)
        line = f.readline()

    for l in lines:
        G.add_node(l[0], color=0, shape='c')
        
    for l in lines:
        N = l[2].split(",")
        W = l[3].split(",")
        for n,w in zip(N, W):
            G.add_edge(l[0], n, weight=w, color=0, width=1, alpha=0.5)
    return 1

def load_log(log_file):
    #split into lines
    try:
        f = open(log_file, "r")
    except IOError:
        print ("Failed to open %s" % log_file)
        return -1

    #split lines into fields
    line = f.readline()
    while (line != ""):
        line = line.strip("\r\n")
        fields = line.split(":")
        exe_script.append(fields)
        line = f.readline()

    return 1

def add_node(node, conn_nodes, weights):
    global pos
    G.add_node(node, color=0, shape='c')
    for n,w in zip(conn_nodes,weights):
        G.add_edge(node, n, weight=w, color=0, width=1, alpha=0.5)
    pos = nx.shell_layout(G)

def del_node(node):
    G.remove_node(node)
    pos = nx.shell_layout(G)

#get stored color for topic/msg combination, generate color if not stored
def get_color(topic_msg):
    if(not(topic_msg in colors)):
        c = random.randint(64,255)
        colors[topic_msg] = c
    return int(colors[topic_msg])

def recv_msg(node, topic_msg, is_sub):
    #switch node to corresponding color
    if( not(node in G.nodes())):
        return

    c = get_color(topic_msg)
    G.nodes[node]['color'] = c
    if (is_sub == 'YES'):
        G.nodes[node]['shape'] = 'd'

    rf_q.append(node)

    print ("recved msg")

def send_msg(s_node, r_node, topic_msg):
    #find edge
    if (not(s_node in G.nodes()) or not(r_node in G.nodes())):
        return

    c = get_color(topic_msg)
    G.edges[s_node, r_node]['color'] = c
    G.edges[r_node, s_node]['color'] = c
    print ("sent_msg")

def ariv_msg(s_node, r_node):
    if (not(s_node in G.nodes()) or not(r_node in G.nodes())):
        return

    G.edges[s_node, r_node]['color'] = 0
    G.edges[r_node, s_node]['color'] = 0

def cycle():
    #reset node, node borders, edge colors at beginning of every cycle
    plt.clf()
    labels = nx.get_edge_attributes(G, 'weight')

    EC = nx.get_edge_attributes(G, 'color')
    ec = []
    for e in G.edges():
        ec.append(EC[e])

    NC = nx.get_node_attributes(G, 'color')
    nc = []

    for n in G.nodes():
        nc.append(NC[n])

    NS = nx.get_node_attributes(G, 'shape')
    ns = []
    for n in G.nodes():
        ns.append(NS[n])

    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_color=nc, node_size=450, labels=G.nodes(), vmin=0, vmax=255, cmap=plt.cm.rainbow, with_labels=True, shape=ns) 
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels) 
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=ec, width=1.0, cmap=plt.cm.rainbow, edge_vmin=0, edge_vmax=255)

def reset():
    for n in rf_q:
        if n in G.nodes():
            G.nodes[n]['color'] = 0
            G.nodes[n]['shape'] = 'c'
    del rf_q[:]

def run_script_line(s_line): 
    if(s_line[1] == 'RECV'):
        recv_msg(s_line[2], s_line[3] + s_line[4], s_line[5])
    elif(s_line[1] == 'SENT'):
        send_msg(s_line[2], s_line[3], s_line[4] + s_line[5])
    elif(s_line[1] == 'ARIV'):
        ariv_msg(s_line[2], s_line[3]) 
    elif(s_line[1] == 'ANODE'):
        add_node(s_line[2], s_line[3].split(","), s_line[4].split(","))
        print (G.nodes())
        print ("anode")
    elif(s_line[1] == 'RNODE'):
        print (s_line[2])
        del_node(s_line[2])        
        print ("rnode")
    else:
        print("Invalid script line: %s" % s_line)

def exe_log():
    pc = 0
    gtime = 0
    counter = 0
    while counter < MAX_CYCLES:
        if(pc < len(exe_script)):
            while(int(exe_script[pc][0]) <= gtime):
                #run all scheduled functions at each given time
                run_script_line(exe_script[pc])
                pc = pc + 1
                if(pc == len(exe_script)):
                    break 
        gtime = gtime + 1
        cycle()
        pause(CYCLE_PERIOD)
        if(REFRESH_NODES == True):
            reset()
        print ("cycle[" + str(counter) + "]")
        counter = counter + 1

#load_topo("topo.txt")
#load_log("log.txt")
load_topo(sys.argv[1])
load_log(sys.argv[2])
if(sys.argv[3] == "True"):
    REFRESH_NODES=True
CYCLE_PERIOD=(float(sys.argv[4]))
pos = nx.shell_layout(G)
pylab.show()
exe_log()
pause(5)

