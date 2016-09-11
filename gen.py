#!/usr/bin/env python
# -*- coding:utf-8 -*--

class Road:
    def __init__(self, src, dst):
        self.src = int(src)
        self.dst = int(dst)

class CityMap:
    def __init__(self, vtx_num, edg_num, edg_prp):
        self.vtx_num = int(vtx_num)
        self.edg_num = int(edg_num)
        self.roads = []
        self.vtx = [[[], []] for i in range(vtx_num)]
        crs_prp = [{} for i in range(edg_num)]
        for i in edg_prp:
            self.roads.append(Road(i[0], i[1]))
        for i, j in enumerate(self.roads):
            self.vtx[j.src][1].append(i)
            self.vtx[j.dst][0].append(i)
        for index, i in enumerate(self.roads):
            for j in self.vtx[i.dst][1]:
                flag = True
                while flag:
                    try:
                        print "\nFrom %d to %d : "%(index,j)
                        crs_prp[index][j] = float(raw_input())
                        flag = False
                    except:
                        pass
        print crs_prp

def main():
    global city_map
    city_map = CityMap(4, 8, [
        [0, 1, 2, 273, 11.11],
        [1, 0, 2, 273, 11.11],
        [1, 2, 2, 433, 11.11],
        [2, 1, 2, 433, 11.11],
        [2, 3, 4, 280, 18.66],
        [3, 2, 4, 280, 18.66],
        [3, 0, 1, 314, 8.33],
        [0, 3, 1, 314, 8.33]
    ])

if __name__ == "__main__":
    main()
