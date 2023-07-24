import sys
import os

class Node():
    def __init__(self, id, seq,):
        self.id = id
        self.seq = seq
        self.mult = 1
        self.prevId = []
        self.succId = []

    def add_succ(self, succId):
        if succId in self.succId:
            return
        self.succId.append(succId)

    def add_prev(self, prevId):
        if prevId in self.prevId:
            return
        self.prevId.append(prevId)

class Tree():
    def __init__(self, k_mere):
        self.k_mere = k_mere
        self.nodes = {}

    def add_node(self, seq):
        seq_inv = ""
        for e in seq:
            if e == "A":
                seq_inv = f"T{seq_inv}"
            if e == "T":
                seq_inv = f"A{seq_inv}"
            if e == "C":
                seq_inv = f"G{seq_inv}"
            if e == "G":
                seq_inv = f"C{seq_inv}"
        if not seq in self.nodes and not seq_inv in self.nodes:
            self.nodes[seq] = Node(id=len(self.nodes),seq=seq)
        else:
            if not seq in self.nodes:
                self.nodes[seq_inv].mult += 1
            else:
                self.nodes[seq].mult += 1
        
    def add_adj(self, seq, prevId, succId):
        seq_inv = ""
        if not seq in self.nodes:
            tmp = succId
            succId = prevId
            prevId = tmp
        for e in seq:
            if e == "A":
                seq_inv = f"T{seq_inv}"
            if e == "T":
                seq_inv = f"A{seq_inv}"
            if e == "C":
                seq_inv = f"G{seq_inv}"
            if e == "G":
                seq_inv = f"C{seq_inv}"
        if prevId != None:
            if not seq in self.nodes:
                self.nodes[seq_inv].add_prev(prevId)
            else:
                self.nodes[seq].add_prev(prevId)
        if succId != None:
            if not seq in self.nodes:
                self.nodes[seq_inv].add_succ(succId)
            else:
                self.nodes[seq].add_succ(succId)
    
    def get_node_id(self, seq):
        seq_inv = ""
        for e in seq:
            if e == "A":
                seq_inv = f"T{seq_inv}"
            if e == "T":
                seq_inv = f"A{seq_inv}"
            if e == "C":
                seq_inv = f"G{seq_inv}"
            if e == "G":
                seq_inv = f"C{seq_inv}"
        if not seq in self.nodes and not seq_inv in self.nodes:
            return len(list(self.nodes))
        else :
            if not seq in self.nodes:
                return self.nodes[seq_inv].id
            else:
                return self.nodes[seq].id

    def run(self, output_file=None):
        file = open(output_file, 'w')
        file.write(f"{len(list(self.nodes))} {self.k_mere}\n")
        # print(len(list(self.nodes)), self.k_mere)
        for node in list(self.nodes):
            id = self.nodes[node].id
            seq = self.nodes[node].seq
            mult = self.nodes[node].mult
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
            file.write(f"{id} {seq} {mult} {prevStr} {succStr}\n")
            # print(
            #     self.nodes[node].id,
            #     self.nodes[node].seq,
            #     self.nodes[node].mult,
            #     self.nodes[node].prevId,
            #     self.nodes[node].succId
            # )
        file.close()

if len(sys.argv) != 4:
    print(f"ERROR format : python3 debruijn_build.py input_file k_mere output_file.")
    exit(1)
elif not os.path.isfile(sys.argv[1]):
    print(f"ERROR file {sys.argv[1]} does not exist.")
    exit(1)

file = open(sys.argv[1], 'r')
k_mere = int(sys.argv[2])

tree = Tree(k_mere)
for line in file:
    if not "@" in line and len(line[:-1]) != 0:
        read = line[:-1]
        offset = 0
        while offset + k_mere < len(read) + 1:
            seq = read[offset:offset+k_mere]
            tree.add_node(seq)
            prevId, succId = None, None
            prev, succ = None, None
            if offset > 0:
                prev = read[offset-1:offset+k_mere-1]
                prevId = tree.get_node_id(prev)
            if offset + k_mere + 1 < len(read) + 1:
                succ = read[offset+1:offset+k_mere+1]
                succId = tree.get_node_id(succ)
            tree.add_adj(seq, prevId, succId)
            offset += 1

tree.run(output_file=sys.argv[3])