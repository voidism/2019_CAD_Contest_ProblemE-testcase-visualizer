import numpy as np
import sys, time


class MyCanvas():
    def __init__(self, file=None, file_out=None, width=1000, height=1000):
        self.idx = 0
        self.name2idx = {"MERGE": 0, "CLIPPER": 1, "SPLIT": 2}
        self.file = open(file, 'r')
        self.file_out = open(file_out, 'r')
        self.mode = None
        self.name = (file, file_out)

        self.in_map = np.zeros((width, height), dtype=np.bool)
        self.out_map = np.zeros((width, height), dtype=np.bool)

    def proc(self):
        for line in self.read():
            self.draw_line(line)
        # print("Input file bitmap built!")

        for line in self.out():
            self.draw_line_rect(line)
        # print("Output file bitmap built!")
        self.verify()

        
    def read(self):
        for line in self.file:
            line = line.strip()
            if len(line) == 0:
                continue
            spt = line.split(' ')
            if spt[0] == "DATA":
                self.mode = spt[1]
            if spt[0] in ["OPERATION", "DATA", "END"]: 
                # print(line)
                pass
            else:
                yield line

    def out(self):
        self.mode = "SPLIT"
        for line in self.file_out:
            line = line.strip()
            if len(line) == 0:
                continue
            spt = line.split(' ')
            assert spt[0] == "RECT"
            # print(line)
            yield line

    def coords2minmax(self, coords):
        x1 = min(*[x[0] for x in coords])
        x2 = max(*[x[0] for x in coords])
        y1 = min(*[x[1] for x in coords])
        y2 = max(*[x[1] for x in coords])
        return x1, x2, y1, y2

    def verify(self):
        res = (self.in_map != self.out_map).sum()
        if res==0:
            print("%s <=> %s verify successfully!"%self.name)
            # import matplotlib.pyplot as plt
            # plt.matshow((self.in_map))
            # plt.show()
            # plt.matshow((self.out_map))
            # plt.show()
        else:
            print("%s <=> %s verify failed! with %d errors" % (self.name[0], self.name[1], res))
            sys.exit(127)
            # import matplotlib.pyplot as plt
            # plt.matshow((self.in_map))
            # plt.show()
            # plt.matshow((self.out_map))
            # plt.show()
            # plt.matshow((self.in_map != self.out_map))
            # plt.show()


    def draw_poly(self, coords):
        x1, x2, y1, y2 = self.coords2minmax(coords)
        if self.mode == "MERGE":
            self.in_map[x1:x2, y1:y2] = True
        elif self.mode == "CLIPPER":
            self.in_map[x1:x2, y1:y2] = False

    def draw_rect(self, coords):
        x1, x2, y1, y2 = self.coords2minmax(coords)
        if self.mode == "SPLIT":
            self.out_map[x1:x2, y1:y2] = True
        
    def draw_line(self, text="POLYGON 131880 539700 137900 539700 137900 541100 131880 541100 131880 539700 ;"):
        vertices = text.split(' ')
        assert vertices[0] in "POLYGON"
        vertices = vertices[1:-1]
        assert len(vertices)%2 == 0 
        coords = [(int(vertices[2 * i]), int(vertices[2 * i + 1])) for i in range(len(vertices) // 2)]
        self.draw_poly(coords)

    def draw_line_rect(self, text="RECT 50 100 200 200 ;"):
        vertices = text.split(' ')
        assert vertices[0] in "RECT"
        vertices = vertices[1:-1]
        assert len(vertices)%2 == 0 
        coords = [(int(vertices[2 * i]), int(vertices[2 * i + 1])) for i in range(len(vertices) // 2)]
        self.draw_rect(coords)


if __name__ == "__main__":
    canvas = MyCanvas(width=int(sys.argv[3]), height=int(sys.argv[3]), file=str(sys.argv[1]), file_out=sys.argv[2])
    canvas.proc()