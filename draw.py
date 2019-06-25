import numpy as np
import cv2
import sys

class Layout():
    def __init__(self, max_size=1000000):
        self.max_size = max_size
        self.colors = [
            (255,0,0),
            (0,255,0),
            (0,0,255),
            (255,255,0),
            (0, -255,255),
            (255, 0, 255),
            (-192,192,192),
            (-128,128,128),
            (128,0,0),
            (128,128,0),
            (0,128,0),
            (128,0,128),
            (0, -128,128),
            (0, 0, 128)
        ]
        self.idx = 0
        self.name2idx = {"MERGE":0, "CLIPPER":1, "SPLIT":2}
        self.canvas = np.zeros((self.max_size, self.max_size, 3), dtype="uint8")

    def get_color(self):
        return self.colors[self.idx % len(self.colors)]

    def draw_poly(self, coords):
        pts = np.array(coords, np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(self.canvas, [pts], True, self.get_color())

    def draw_rect(self, coords):
        cv2.rectangle(self.canvas, coords[0], coords[1], self.get_color(), 3)

    def draw_line(self, text="POLYGON 131880 539700 137900 539700 137900 541100 131880 541100 131880 539700 ;"):
        vertices = text.split(' ')
        assert vertices[0] in "POLYGON"
        vertices = vertices[1:-1]
        assert len(vertices)%2 == 0 
        coords = [(int(vertices[2 * i]), int(vertices[2 * i + 1])) for i in range(len(vertices) // 2)]
        if coords[0] == coords[-1]:
            coords.pop(-1)
        self.draw_poly(coords)

    def draw_line_rect(self, text="RECT 50 100 200 200 ;"):
        vertices = text.split(' ')
        assert vertices[0] in "RECT"
        vertices = vertices[1:-1]
        assert len(vertices)%2 == 0 
        coords = [(int(vertices[2 * i]), int(vertices[2 * i + 1])) for i in range(len(vertices) // 2)]
        print(coords)
        self.draw_rect(coords)

    def show_wait(self):
        cv2.imshow("Canvas", self.canvas)
        cv2.waitKey(10000)

'''
OPERATION M1 M2 C1 C2 SH ;

DATA MERGE M1 ;
POLYGON 1036000 1000 4193980 1000 4193980 1700 1036000 1700 1036000 1000 ;
'''

    
class TestCase():
    def __init__(self, file, file_out, size):
        self.layout = Layout(max_size=size)
        self.file = open(file, 'r')
        self.file_out = open(file_out, 'r')
        
    def read(self):
        for line in self.file:
            line = line.strip()
            if len(line) == 0:
                continue
            spt = line.split(' ')
            if spt[0] == "DATA":
                self.layout.idx = self.layout.name2idx[spt[1]]
            if spt[0] in ["OPERATION", "DATA", "END"]: 
                print(line)
            else:
                self.layout.draw_line(line)
                self.layout.show_wait()

    def out(self):
        self.layout.idx = self.layout.name2idx["SPLIT"]
        for line in self.file_out:
            line = line.strip()
            if len(line) == 0:
                continue
            spt = line.split(' ')
            assert spt[0] == "RECT"
            print(line)
            self.layout.draw_line_rect(line)
            self.layout.show_wait()

if __name__ == "__main__":
    t = TestCase(file=str(sys.argv[1]), file_out=sys.argv[2], size=int(sys.argv[3]))
    t.read()
    t.out()
    cv2.destroyAllWindows()