# import numpy as np
from tkinter import *
import sys, time

root = Tk()

colors = [
"#FF0000",
"#00FF00",
"#0000FF",
"#FFFF00",
"#00FFFF",
"#FF00FF",
"#C0C0C0",
"#808080",
"#800000",
"#800000",
"#808000",
"#008000",
"#800080",
"#008080",
"#000080"
]

class MyCanvas(Canvas):
    def __init__(self, master=None, file=None, file_out=None, width=1000, height=1000):
        Canvas.__init__(self, master, width=1000, height=1000)
        # self.max_size = max_size
        self.idx = 0
        self.name2idx = {"MERGE": 0, "CLIPPER": 1, "SPLIT": 2}
        self.keypress = False
        self.bind("<Key>", self.key)
        self.pack()
        self.focus_set()
        self.file = open(file, 'r')
        self.file_out = open(file_out, 'r')
        self.riter = self.read()
        self.oiter = self.out()
        self.c = False

    def key(self, event):
        c = repr(event.char)
        print("pressed", c)
        if c == "'r'":
            try:
                line = next(self.riter)
                self.draw_line(line)
            except:
                c = "'w'"
        if c == "'w'":
            try:
                line = next(self.oiter)
                self.draw_line_rect(line, c=self.c)
                self.c = not self.c
            except:
                c = "'e'"
                # pass
        if c == "'e'":
            sys.exit()
        
    def read(self):
        for line in self.file:
            line = line.strip()
            if len(line) == 0:
                continue
            spt = line.split(' ')
            if spt[0] == "DATA":
                self.idx = self.name2idx[spt[1]]
            if spt[0] in ["OPERATION", "DATA", "END"]: 
                print(line)
            else:
                yield line
                # self.draw_line(line)
                # self.show_wait()

    def out(self):
        self.idx = self.name2idx["SPLIT"]
        for line in self.file_out:
            line = line.strip()
            if len(line) == 0:
                continue
            spt = line.split(' ')
            assert spt[0] == "RECT"
            print(line)
            yield line
            yield line
            # self.draw_line_rect(line)
            # time.sleep(1)
            # self.show_wait()

    # def scaling(xy):
    #     ret = (xy[0] // self.scale, xy[1] // self.scale)
    #     print("lll: ", ret)
    #     return ret

    def get_color(self):
        return colors[self.idx % len(colors)]

    def draw_poly(self, coords):
        # pts = np.array(coords, np.int32)
        # pts = pts.reshape((-1,1,2))
        self.create_polygon([x for y in coords for x in y], fill=self.get_color(), outline="#000000")

    def draw_rect(self, coords, c=False):
        if c:
            self.create_rectangle(*[x for y in coords for x in y], fill="#FFFFFF", outline="#FFFFFF")
        else:
            self.create_rectangle(*[x for y in coords for x in y], fill=self.get_color(), outline="#000000")

    def draw_line(self, text="POLYGON 131880 539700 137900 539700 137900 541100 131880 541100 131880 539700 ;"):
        print(text)
        vertices = text.split(' ')
        assert vertices[0] in "POLYGON"
        vertices = vertices[1:-1]
        assert len(vertices)%2 == 0 
        coords = [(int(vertices[2 * i]), int(vertices[2 * i + 1])) for i in range(len(vertices) // 2)]
        # if coords[0] == coords[-1]:
        #     coords.pop(-1)
        print(coords)
        self.draw_poly(coords)

    def draw_line_rect(self, text="RECT 50 100 200 200 ;", c=False):
        vertices = text.split(' ')
        assert vertices[0] in "RECT"
        vertices = vertices[1:-1]
        assert len(vertices)%2 == 0 
        coords = [(int(vertices[2 * i]), int(vertices[2 * i + 1])) for i in range(len(vertices) // 2)]
        print(coords)
        self.draw_rect(coords, c)

'''
OPERATION M1 M2 C1 C2 SH ;

DATA MERGE M1 ;
POLYGON 1036000 1000 4193980 1000 4193980 1700 1036000 1700 1036000 1000 ;
'''
# root.mainloop()

class TestCase():
    def __init__(self, file, file_out, size):
        self.file = open(file, 'r')
        self.file_out = open(file_out, 'r')
        
    def read(self):
        for line in self.file:
            line = line.strip()
            if len(line) == 0:
                continue
            spt = line.split(' ')
            if spt[0] == "DATA":
                canvas.idx = canvas.name2idx[spt[1]]
            if spt[0] in ["OPERATION", "DATA", "END"]: 
                print(line)
            else:
                canvas.draw_line(line)
                canvas.show_wait()

    def out(self):
        canvas.idx = canvas.name2idx["SPLIT"]
        for line in self.file_out:
            line = line.strip()
            if len(line) == 0:
                continue
            spt = line.split(' ')
            assert spt[0] == "RECT"
            print(line)
            canvas.draw_line_rect(line)
            canvas.show_wait()

if __name__ == "__main__":
    # t = TestCase(file=str(sys.argv[1]), file_out=sys.argv[2], size=int(sys.argv[3]))
    # t.read()
    # t.out()
    canvas = MyCanvas(root, width=int(sys.argv[3]), height=int(sys.argv[3]), file=str(sys.argv[1]), file_out=sys.argv[2])
    root.mainloop()