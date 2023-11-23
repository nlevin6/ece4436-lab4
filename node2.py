from utils import TRACE, YES, NO, Rtpkt, tolayer2, clocktime


class DistanceTable:
    costs = [[0 for j in range(4)] for i in range(4)]


dt = DistanceTable()

# students to write the following two routines, and maybe some others

# modify this statement for different node
edges = [3, 1, 0, 2]
min_costs = [0, 0, 0, 0]
node_id = 2
pkt2 = [Rtpkt(2, i, [0, 0, 0, 0]) for i in range(4)]


def sendpkt():
    global pkt2, min_costs
    # make the packets
    for i in range(4):
        pkt2[i].sourceid = node_id
        pkt2[i].destid = i
        pkt2[i].mincost = min_costs[:]

    # send the packets
    for i in range(4):
        if i != node_id:  # if not sending to itself
            tolayer2(pkt2[i])
            print(f"At time t={clocktime:.3f}, node {pkt2[i].sourceid} sends packet to node {pkt2[i].destid} with: "
                  f"({pkt2[i].mincost[0]}  {pkt2[i].mincost[1]}  {pkt2[i].mincost[2]}  {pkt2[i].mincost[3]})")


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
def rtinit2():
    global dt, edges
    print(f"rtinit0() called at {clocktime}\n")
    for i in range(4):
        for j in range(4):
            if i == j:
                dt.costs[i][j] = edges[i]
            else:
                dt.costs[i][j] = 999

    printdt2(dt)  # print the distance table after initialization

    # calculate min costs
    for i in range(4):
        min_costs[i] = min(dt.costs[i])

    # send packets
    sendpkt()


def rtupdate2(rcvdpkt):
    global dt
    src, dest, mincost = rcvdpkt.sourceid, rcvdpkt.destid, rcvdpkt.mincost
    print(f"rtupdate0() is called at time t=: {clocktime:.3f} as node {src} sent a pkt with: "
          f"({mincost[0]} {mincost[1]} {mincost[2]} {mincost[3]})")

    # update distance table
    for i in range(4):
        possible_new_dist = mincost[i] + dt.costs[src][src]
        if possible_new_dist < 999:
            dt.costs[i][src] = possible_new_dist
        else:
            dt.costs[i][src] = 999

    printdt2(dt)  # print the distance table after updating

    calc_send_pkt()


def printdt2(dtptr):
    print("                via     \n")
    print("   D2 |    0     1    3 \n")
    print("  ----|-----------------\n")
    print("     0|  %3d   %3d   %3d\n" %
          (dtptr.costs[0][0], dtptr.costs[0][1], dtptr.costs[0][3]))
    print("dest 1|  %3d   %3d   %3d\n" %
          (dtptr.costs[1][0], dtptr.costs[1][1], dtptr.costs[1][3]))
    print("     3|  %3d   %3d   %3d\n" %
          (dtptr.costs[3][0], dtptr.costs[3][1], dtptr.costs[3][3]))
