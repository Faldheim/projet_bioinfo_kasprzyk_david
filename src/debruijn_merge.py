import sys
import os

class Node():
    def __init__(self, id, seq, mult, prevId, succId):
        self.id = id
        self.seq = seq
        self.mult = []
        self.prevId = []
        self.succId = []
        for m in mult:
            self.mult.append(m)
        for p in prevId:
            self.prevId.append(p)
        for s in succId:
            self.succId.append(s)

    def reverse(self):
        seq_inv = ""
        for e in self.seq:
            if e == "A":
                seq_inv = f"T{seq_inv}"
            if e == "T":
                seq_inv = f"A{seq_inv}"
            if e == "C":
                seq_inv = f"G{seq_inv}"
            if e == "G":
                seq_inv = f"C{seq_inv}"
        return Node(
            self.id,
            seq_inv,
            self.mult[::-1],
            succId=self.prevId[::-1],
            prevId=self.succId[::-1],
        )

class Tree():
    def __init__(self, k_mere):
        self.k_mere = k_mere
        self.nodes = {}

    def add_node(self, id, seq, mult, prevId, succId):
        self.nodes[id] = Node(
            id=id,
            seq=seq,
            mult=[mult],
            prevId=prevId,
            succId=succId,
        )

    def merge(self):
        offset = 0
        while offset < len(list(self.nodes)):
            id = list(self.nodes)[offset]
            node = self.nodes[id]
            inf_pop = 0
            # print("=================")
            # print(node.id, node.seq, node.prevId, node.succId)
            while len(node.prevId) == 1:
                prevNodeId = node.prevId[0]
                prevNode = self.nodes[prevNodeId]
                # print('----------------')
                # print(prevNode.id, prevNode.seq, prevNode.prevId, prevNode.succId)
                if not id in prevNode.succId:
                    prevNode = prevNode.reverse()
                if len(prevNode.succId) != 1:
                    break

                seq = f"{prevNode.seq[0:1+max(len(prevNode.seq)-len(node.seq),0)]}{node.seq}"
                mult = []
                for i in prevNode.mult:
                    mult.append(i)
                for i in node.mult:
                    mult.append(i)
                prevId = prevNode.prevId
                succId = node.succId

                node = Node(id,seq,mult,prevId,succId)
                if id > prevNodeId:
                    inf_pop += 1
                self.nodes.pop(prevNodeId)
                if len(node.prevId) == 0:
                    tmp = node.reverse()
                    if len(tmp.prevId) == 1:
                        node = tmp
                self.nodes[id] = node
                for i in prevId:
                    for j in range(len(self.nodes[i].prevId)):
                        if self.nodes[i].prevId[j] == prevNodeId:
                            self.nodes[i].prevId[j] = id
                    for j in range(len(self.nodes[i].succId)):
                        if self.nodes[i].succId[j] == prevNodeId:
                            self.nodes[i].succId[j] = id
            
            while len(node.succId) == 1:
                succNodeId = node.succId[0]
                succNode = self.nodes[succNodeId]
                if not id in succNode.prevId:
                    succNode = succNode.reverse()
                if len(succNode.prevId) != 1:
                    break

                seq = f"{node.seq}{succNode.seq[len(succNode.seq)-1-max(len(succNode.seq)-len(node.seq),0):]}"
                mult = []
                for i in node.mult:
                    mult.append(i)
                for i in succNode.mult:
                    mult.append(i)
                succId = succNode.succId
                prevId = node.prevId

                node = Node(id,seq,mult,prevId,succId)
                if id > succNodeId:
                    inf_pop += 1
                self.nodes.pop(succNodeId)
                if len(node.succId) == 0:
                    tmp = node.reverse()
                    if len(tmp.succId) == 1:
                        node = tmp
                self.nodes[id] = node
                for i in succId:
                    for j in range(len(self.nodes[i].succId)):
                        if self.nodes[i].succId[j] == succNodeId:
                            self.nodes[i].succId[j] = id
                    for j in range(len(self.nodes[i].prevId)):
                        if self.nodes[i].prevId[j] == succNodeId:
                            self.nodes[i].prevId[j] = id

            offset += 1 - inf_pop
        return

    def rearrange(self):
        id = 0
        assos = {}
        for i in list(self.nodes):
            assos[i] = id
            id += 1

        old_nodes = self.nodes
        new_nodes = {}

        for i in list(old_nodes):
            prevId = old_nodes[i].prevId
            for j in range(len(prevId)):
                prevId[j] = assos[prevId[j]]
            succId = old_nodes[i].succId
            for j in range(len(succId)):
                succId[j] = assos[succId[j]]
            new_nodes[assos[i]] = Node(
                id=assos[i],
                seq=old_nodes[i].seq,
                mult=old_nodes[i].mult,
                prevId=prevId,
                succId=succId
            )

        self.nodes = new_nodes
        return     

    def run(self, output_file=None):
        file = open(output_file, 'w')
        file.write(f"{len(list(self.nodes))} {self.k_mere}\n")
        # print(len(list(self.nodes)), k_mere)
        for node in list(self.nodes):
            id = self.nodes[node].id
            seq = self.nodes[node].seq
            mult = self.nodes[node].mult
            multStr = ""
            for i in range(len(mult)):
                if i == 0:
                    multStr = f"{mult[i]}"
                else:
                    multStr = f"{multStr},{mult[i]}"
            prevStr = ""
            for i in range(len(self.nodes[node].prevId)):
                if i == 0:
                    prevStr = f"{self.nodes[node].prevId[i]}"
                else:
                    prevStr = f"{prevStr},{self.nodes[node].prevId[i]}"
            succStr = ""
            for i in range(len(self.nodes[node].succId)):
                if i == 0:
                    succStr = f"{self.nodes[node].succId[i]}"
                else:
                    succStr = f"{succStr},{self.nodes[node].succId[i]}"
            file.write(f"{id} {seq} {multStr} {prevStr} {succStr}\n")
            # print(
            #     self.nodes[node].id,
            #     self.nodes[node].seq,
            #     self.nodes[node].mult,
            #     self.nodes[node].prevId,
            #     self.nodes[node].succId
            # )
        file.close()

# =================================================================

if len(sys.argv) != 3:
    print(f"ERROR format : python3 debruijn_merge.py input_file output_file.")
    exit(1)
elif not os.path.isfile(sys.argv[1]):
    print(f"ERROR file {sys.argv[1]} does not exist.")
    exit(1)

file = open(sys.argv[1], 'r')
read = file.readline()[:-1].split(' ')
k_mere = int(read[1])

tree = Tree(k_mere)
for line in file:
    read = line[:-1].split(' ')
    id, seq, mult, prevIdStr, succIdStr = read
    prevId, succId = prevIdStr.split(','), succIdStr.split(',')

    id, mult = int(id), int(mult)
    if '' in prevId:
        prevId = []
    else:
        for i in range(len(prevId)):
            prevId[i] = int(prevId[i])
    if '' in succId:
        succId = []
    else:
        for i in range(len(succId)):
            succId[i] = int(succId[i])
    # print(id,seq,mult,prevId,succId)
    tree.add_node(id,seq,mult,prevId,succId)

tree.merge()
tree.rearrange()
tree.run(output_file=sys.argv[2])