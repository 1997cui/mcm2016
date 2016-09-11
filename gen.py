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
                crs_prp[index][j] = 0
        print crs_prp

def main():
    global city_map
    city_map = CityMap(4, 8, [
        [0, 1, 1, 407, 8.33],
        [1, 0, 1, 407, 8.33],
        [1, 2, 1, 277, 8.33],
        [2, 1, 1, 277, 8.33],
        [2, 3, 4, 416, 16.66],
        [3, 2, 4, 416, 16.66],
        [3, 0, 2, 300, 13.89],
        [0, 3, 2, 300, 13.89]])

if __name__ == "__main__":
    main()
