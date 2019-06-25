from tkinter import *
import sys

root = Tk()

colours = [
"#000000",
"#FFFFFF",
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
    def __init__(self, master=None, width=1000, height=1000):
        Canvas.__init__(self, master, width=1000, height=1000)
        self.operations = []
        self.bind("<Key>", self.key)
        self.bind("<Button-1>", self.callback)
        self.pack()
        self.focus_set()
        self.mid = 1
        self.cid = 1
        self.end = False

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

    def key(self, event):
        c = repr(event.char)
        print("pressed", c)
        if c == "'e'":
            if self.operations[-1]['polys'] == [[]]:
                print("last op ends with no polys.")
                return
            if len(self.operations[-1]['polys'][-1]) == 4:
                print("add one more point.")
                return
            # add first line
            startx, starty = self.operations[-1]['polys'][-1][:2]
            secx, secy = self.operations[-1]['polys'][-1][2:4]
            lastx, lasty = self.operations[-1]['polys'][-1][-2:]
            newx, newy = (lastx, starty) if secy != starty else (startx, lasty)
            # n2x, n2y = (lastx, starty) if secy == starty else (startx, lasty)
            self.operations[-1]['polys'][-1] += [newx, newy]
            self.create_line(lastx, lasty, newx, newy, fill=colours[self.cid + self.mid])
            # add second line
            self.operations[-1]['polys'][-1] += [startx, starty]
            self.create_line(newx, newy, startx, starty, fill=colours[self.cid + self.mid])
            self.operations[-1]['polys'][-1] = self.remove_redundent(self.operations[-1]['polys'][-1])
            self.end = True

        elif c == "'m'":
            print("ADD MERGE: M%d"%self.mid)
            self.operations.append({"name": "M%d" % self.mid, "polys": [[]]})
            self.mid += 1
            self.end = False
        elif c == "'c'":
            print("ADD CLIP: C%d"%self.mid)
            self.operations.append({"name":"C%d"%self.cid, "polys":[[]]})
            self.cid += 1
            self.end = False


    def callback(self, event):
        print("clicked at", event.x, event.y)
        if self.end:
            self.operations[-1]['polys'].append([])
            self.end = False
        if len(self.operations) == 0:
            print("add operation before click.")
        else:
            if len(self.operations[-1]['polys'][-1]) == 0:
                self.operations[-1]['polys'][-1] += [event.x, event.y]
                self.create_text(event.x, event.y, text=self.operations[-1]['name'], fill=colours[self.cid + self.mid])
            else:
                lastx, lasty = self.operations[-1]['polys'][-1][-2:]
                dx, dy = abs(event.x - lastx), abs(event.y - lasty)
                newx, newy = (lastx, event.y) if dx < dy else(event.x, lasty)
                self.operations[-1]['polys'][-1] += [newx, newy]
                self.create_line(lastx, lasty, newx, newy, fill=colours[self.cid + self.mid])

def dict2testcase(di, filename):
    f = open(filename, 'w')
    f.write("OPERATION " + ' '.join([x['name'] for x in di]) + " SV ;\n\n")
    for item in di:
        f.write("DATA " + ("MERGE" if (item['name'][0] == "M") else "CLIPPER") + " %s ;\n" % (item['name']))
        for term in item["polys"]:
            f.write("POLYGON " + ' '.join([str(x) for x in term]) + " ;\n")
        f.write("END DATA\n\n")
    f.close()





if __name__ == "__main__":
    assert len(sys.argv) >= 2
    canvas= MyCanvas(root, width=1000, height=1000)
    root.mainloop()

    print(canvas.operations)
    dict2testcase(canvas.operations, sys.argv[1])
