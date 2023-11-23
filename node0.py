from utils import TRACE, YES, NO, Rtpkt, tolayer2, clocktime


class DistanceTable:
    costs = [[0 for j in range(4)] for i in range(4)]


dt = DistanceTable()

# students to write the following two routines, and maybe some others

# modify this statement for different node
edges = [0, 1, 3, 7]
min_costs = [0, 0, 0, 0]  # new min costs will be stored and overwritten here each time
node_id = 0
pkt0 = [Rtpkt(0, i, [0, 0, 0, 0]) for i in range(4)]


def sendpkt():
    global pkt0, min_costs
    # make the packets
    for i in range(4):
        pkt0[i].sourceid = node_id
        pkt0[i].destid = i
        pkt0[i].mincost = min_costs[:]

    # send the packets
    for i in range(4):
        if i != node_id:  # if not sending to itself
            tolayer2(pkt0[i])
            print(f"At time t={clocktime:.3f}, node {pkt0[i].sourceid} sends packet to node {pkt0[i].destid} with: "
                  f"({pkt0[i].mincost[0]}  {pkt0[i].mincost[1]}  {pkt0[i].mincost[2]}  {pkt0[i].mincost[3]})")


# this function calculates the min costs and sends the packets
def calc_send_pkt():
    global min_costs
    old_min_costs = min_costs.copy()  # make a copy of the old min costs
    for i in range(4):
        min_costs[i] = min(dt.costs[i])  # calculate the new min costs
        if old_min_costs[i] != min_costs[i]:  # if the new min costs are different from the old ones, send the packet
            sendpkt()
        else:
            print(f"minimum costs of node {i} did not change, no packet sent")


def rtinit0():
    global dt, edges
    print(f"rtinit0() called at {clocktime}\n")
    for i in range(4):
        for j in range(4):
            if i == j:
                dt.costs[i][j] = edges[i]  # set the diagonal to the edges
            else:
                dt.costs[i][j] = 999

    printdt0(dt)  # print the distance table after initialization

    # calculate min costs
    for i in range(4):
        min_costs[i] = min(dt.costs[i])

    # send packets
    sendpkt()


def rtupdate0(rcvdpkt):
    global dt
    src, dest, mincost = rcvdpkt.sourceid, rcvdpkt.destid, rcvdpkt.mincost
    print(f"rtupdate0() is called at time t=: {clocktime:.3f} as node {src} sent a pkt with: "
          f"({mincost[0]} {mincost[1]} {mincost[2]} {mincost[3]})")

    # update distance table
    for i in range(4):
        # POTENTIAL new distance is the min cost of the sender + the distance from the sender to the current node
        possible_new_dist = mincost[i] + dt.costs[src][src]
        if possible_new_dist < 999:  # if the new distance is less than infinity
            dt.costs[i][src] = possible_new_dist  # update the distance table
        else:
            dt.costs[i][src] = 999

    printdt0(dt)  # print the distance table after updating

    calc_send_pkt()


def printdt0(dtptr):
    print("                via     \n")
    print("   D0 |    1     2    3 \n")
    print("  ----|-----------------\n")
    print("     1|  %3d   %3d   %3d\n" %
          (dtptr.costs[1][1], dtptr.costs[1][2], dtptr.costs[1][3]))
    print("dest 2|  %3d   %3d   %3d\n" %
          (dtptr.costs[2][1], dtptr.costs[2][2], dtptr.costs[2][3]))
    print("     3|  %3d   %3d   %3d\n" %
          (dtptr.costs[3][1], dtptr.costs[3][2], dtptr.costs[3][3]))


# handler for changes in link costs. gets called when link cost between node 0 and other nodes changes
def linkhandler0(linkid, newcost):
    global dt
    # old distance from node 0 to other nodes via linkid
    old_dist = [dt.costs[i][linkid] - dt.costs[linkid][linkid] for i in range(4)]
    new_dist = newcost

    for i in range(4):
        dt.costs[i][linkid] = new_dist + old_dist[i]  # update the distance table

    printdt0(dt)
    calc_send_pkt()
