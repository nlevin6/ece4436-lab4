from utils import TRACE, YES, NO, Rtpkt, tolayer2, clocktime


class DistanceTable:
    costs = [[0 for j in range(4)] for i in range(4)]


dt = DistanceTable()

# students to write the following two routines, and maybe some others

# modify this statement for different node
edges = [7, 999, 2, 0]
node_id = 3


# costs to nodes
def rtinit3():
    global dt, edges
    rtpacket = Rtpkt(0, 0, [edges[0], edges[1], edges[2], edges[3]])

    for j in range(4):
        for k in range(4):
            dt.costs[j][k] = 999

    dt.costs[node_id][0] = edges[0]
    dt.costs[node_id][1] = edges[1]
    dt.costs[node_id][2] = edges[2]
    dt.costs[node_id][3] = edges[3]

    # For each neighbor source is "me" (must change in other files)
    rtpacket.sourceid = node_id
    rtpacket.mincost[0] = dt.costs[rtpacket.sourceid][0]
    rtpacket.mincost[1] = dt.costs[rtpacket.sourceid][1]
    rtpacket.mincost[2] = dt.costs[rtpacket.sourceid][2]
    rtpacket.mincost[3] = dt.costs[rtpacket.sourceid][3]

    for i in range(4):
        if i != rtpacket.sourceid and dt.costs[rtpacket.sourceid][i] != 999:
            rtpacket.destid = i
            tolayer2(rtpacket)

    print(f"rtinit{rtpacket.sourceid} called at {clocktime}\n")
    printdt3(dt)  # print the distance table after initialization


def rtupdate3(rcvdpkt):
    global dt
    rtpacket = Rtpkt(0, 0, [dt.costs[0][0], dt.costs[0][1], dt.costs[0][2], dt.costs[0][3]])

    v = rcvdpkt.sourceid
    x = node_id
    DV_Changed = False

    # Update the location in my cost table
    dt.costs[v][0] = rcvdpkt.mincost[0]
    dt.costs[v][1] = rcvdpkt.mincost[1]
    dt.costs[v][2] = rcvdpkt.mincost[2]
    dt.costs[v][3] = rcvdpkt.mincost[3]

    c_v_x = dt.costs[x][v]

    for y in range(4):
        if y != x:
            D_x_y = dt.costs[x][y]
            D_v_y = dt.costs[v][y]
            new_D_x_y = c_v_x + D_v_y

            if new_D_x_y < D_x_y:
                dt.costs[x][y] = new_D_x_y
                DV_Changed = True

    print(f"rtupdate{node_id} called at {clocktime}")
    print(f"Node {node_id} received packet from node {rcvdpkt.sourceid}")
    if DV_Changed:
        rtpacket.sourceid = node_id
        rtpacket.mincost[0] = dt.costs[rtpacket.sourceid][0]
        rtpacket.mincost[1] = dt.costs[rtpacket.sourceid][1]
        rtpacket.mincost[2] = dt.costs[rtpacket.sourceid][2]
        rtpacket.mincost[3] = dt.costs[rtpacket.sourceid][3]

        for i in range(4):
            if i != rtpacket.sourceid and dt.costs[rtpacket.sourceid][i] != 999:
                rtpacket.destid = i
                tolayer2(rtpacket)

    print(f"Node {node_id}'s distance table has been updated.")
    printdt3(dt)  # Add this line to print the distance table after an update


def printdt3(dtptr):
    print("             via     \n")
    print("   D3 |    0     2 \n")
    print("  ----|-----------\n")
    print("     0|  %3d   %3d\n" % (dtptr.costs[0][0], dtptr.costs[0][2]))
    print("dest 1|  %3d   %3d\n" % (dtptr.costs[1][0], dtptr.costs[1][2]))
    print("     2|  %3d   %3d\n" % (dtptr.costs[2][0], dtptr.costs[2][2]))
