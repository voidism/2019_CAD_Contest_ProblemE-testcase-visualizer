import sys
import random
import numpy as np

class MyCanvas():
    def __init__(self, width=1000, height=1000):
        self.operations = []
        self.mid = 1
        self.cid = 1
        self.end = False
        self.width = width
        self.height = height

    def remove_redundent(self, l):
        assert len(l) % 2 == 0
        to_rm = []
        for i in range(len(l) // 2 - 2):
            if (l[2 * i] == l[2 * i + 2] == l[2 * i + 4]) or (l[2 * i + 1] == l[2 * i + 3] == l[2 * i + 5]):
                to_rm.append(2 * i + 2)
                to_rm.append(2 * i + 3)
        for i in to_rm:
            l.pop(i)
        return l


    def add_merge(self):
        # print("ADD MERGE: M%d"%self.mid)
        self.operations.append({"name": "M%d" % self.mid, "polys": [[]]})
        self.mid += 1
        self.end = False
    
    def add_clip(self):
        # print("ADD CLIP: C%d"%self.cid)
        self.operations.append({"name":"C%d"%self.cid, "polys":[[]]})
        self.cid += 1
        self.end = False

    def random_add(self, n_loop=3, n_rect=5, scale=10):
        for i_loop in range(n_loop):
            self.add_merge()
            for i_rect in range(n_rect):
                x1 = 0; x2 = 0; y1 = 0; y2 = 0
                while not x1 != x2:
                    x1, x2 = sorted(list(np.random.choice(self.width//scale, 2, replace=False))) #sorted([random.randint(1, 999), random.randint(1, 999)])
                while not y1 != y2:
                    y1, y2 = sorted(list(np.random.choice(self.height//scale, 2, replace=False)))# sorted([random.randint(1, 999), random.randint(1, 999)])
                assert x1 != x2
                assert y1 != y2
                self.add_rect(x1*scale, x2*scale, y1*scale, y2*scale)
            self.add_clip()
            for i_rect in range(n_rect):
                x1 = 0; x2 = 0; y1 = 0; y2 = 0
                while not x1 != x2:
                    x1, x2 = sorted(list(np.random.choice(self.width//scale, 2, replace=False))) #sorted([random.randint(1, 999), random.randint(1, 999)])
                while not y1 != y2:
                    y1, y2 = sorted(list(np.random.choice(self.height//scale, 2, replace=False)))# sorted([random.randint(1, 999), random.randint(1, 999)])
                assert x1 != x2
                assert y1 != y2
                self.add_rect(x1*scale, x2*scale, y1*scale, y2*scale)

    def add_rect(self, x1, x2, y1, y2):
        assert x1 != x2
        assert y1 != y2
        if self.end:
            self.operations[-1]['polys'].append([])
            self.end = False
        if len(self.operations) == 0:
            print("add operation before click.")
        else:
            if len(self.operations[-1]['polys'][-1]) == 0:
                self.operations[-1]['polys'][-1] += [x1, y1, x1, y2, x2, y2, x2, y1, x1, y1]
                self.end = True

def dict2testcase(di, filename):
    f = open(filename, 'w')
    f.write("OPERATION " + ' '.join([x['name'] for x in di]) + " SO ;\n\n")
    for item in di:
        f.write("DATA " + ("MERGE" if (item['name'][0] == "M") else "CLIPPER") + " %s ;\n" % (item['name']))
        for term in item["polys"]:
            f.write("POLYGON " + ' '.join([str(x) for x in term]) + " ;\n")
        f.write("END DATA\n\n")
    f.close()





if __name__ == "__main__":
    assert len(sys.argv) >= 4
    canvas= MyCanvas(width=1000, height=600)
    canvas.random_add(int(sys.argv[2]), int(sys.argv[3]))

    # print(canvas.operations)
    dict2testcase(canvas.operations, sys.argv[1])
