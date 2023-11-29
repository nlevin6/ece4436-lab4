import utils
from utils import TRACE, YES, NO, Rtpkt, tolayer2


class DistanceTable:
    costs = [[0 for j in range(4)] for i in range(4)]


dt = DistanceTable()

# modify this statement for different node
edges = [1, 0, 1, 999]
min_costs = [0, 0, 0, 0]
node_id = 1
pkt1 = [Rtpkt(1, i, [0, 0, 0, 0]) for i in range(4)]


def sendpkt():
    global pkt1, min_costs
    # make the packets
    for i in range(4):
        pkt1[i].sourceid = node_id
        pkt1[i].destid = i
        pkt1[i].mincost = min_costs[:]

    # send the packets
    for i in range(3):  # no packet to last node
        if i != node_id:  # if not sending to itself
            tolayer2(pkt1[i])
            print(f"At time t={utils.clocktime:.3f}, node {pkt1[i].sourceid} sends packet to node {pkt1[i].destid} with: "
                  f"({pkt1[i].mincost[0]}  {pkt1[i].mincost[1]}  {pkt1[i].mincost[2]}  {pkt1[i].mincost[3]})")


def calc_send_pkt():
    global min_costs
    old_min_costs = min_costs.copy()
    for i in range(4):
        min_costs[i] = min(dt.costs[i])
        if old_min_costs[i] != min_costs[i]:
            sendpkt()
        else:
            print(f"minimum costs of node {i} did not change, no packet sent")


# costs to nodes
def rtinit1():
    global dt, edges
    print(f"rtinit0() called at {utils.clocktime}\n")
    for i in range(4):
        for j in range(4):
            if i == j:
                dt.costs[i][j] = edges[i]
            else:
                dt.costs[i][j] = 999

    printdt1(dt)  # print the distance table after initialization

    # calculate min costs
    for i in range(4):
        min_costs[i] = min(dt.costs[i])

    # send packets
    sendpkt()


def rtupdate1(rcvdpkt):
    global dt
    src, dest, mincost = rcvdpkt.sourceid, rcvdpkt.destid, rcvdpkt.mincost
    print(f"rtupdate0() is called at time t=: {utils.clocktime:.3f} as node {src} sent a pkt with: "
          f"({mincost[0]} {mincost[1]} {mincost[2]} {mincost[3]})")

    # update distance table
    for i in range(4):
        possible_new_dist = mincost[i] + dt.costs[src][src]
        if possible_new_dist < 999:
            dt.costs[i][src] = possible_new_dist
        else:
            dt.costs[i][src] = 999

    printdt1(dt)  # print the distance table after updating

    calc_send_pkt()


def printdt1(dtptr):
    print("             via   \n")
    print("   D1 |    0     2 \n")
    print("  ----|-----------\n")
    print("     0|  %3d   %3d\n" % (dtptr.costs[0][0], dtptr.costs[0][2]))
    print("dest 2|  %3d   %3d\n" % (dtptr.costs[2][0], dtptr.costs[2][2]))
    print("     3|  %3d   %3d\n" % (dtptr.costs[3][0], dtptr.costs[3][2]))


# handler for changes in link costs. gets called when link cost between node 1 and other nodes changes
def linkhandler1(linkid, newcost):
    global dt
    old_dist = [dt.costs[i][linkid] - dt.costs[linkid][linkid] for i in range(4)]
    new_dist = newcost

    for i in range(4):
        dt.costs[i][linkid] = new_dist + old_dist[i]

    printdt1(dt)
    calc_send_pkt()
