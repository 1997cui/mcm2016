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
    city_map = CityMap(8, 18, [
        [5, 0, 99, 2, 11.11],
        [0, 5, 99, 2, 11.11],
        [1, 5, 170, 1, 11.11],
        [5, 1, 170, 1, 11.11],
        [2, 1, 416, 1, 11.11],
        [1, 2, 416, 1, 11.11],
        [2, 4, 60, 4, 18.66],
        [4, 2, 60, 4, 18.66],
        [4, 3, 224, 4, 18.66],
        [3, 4, 224, 4, 18.66],
        [3, 0, 330, 1, 8.33],
        [0, 3, 330, 1, 8.33],
        [4, 7, 89, 1, 5],
        [7, 4, 89, 1, 5],
        [7, 6, 330, 1, 5],
        [6, 7, 290, 1, 5],
        [6, 5, 90, 1, 5],
        [5, 6, 90, 1, 5]])

if __name__ == "__main__":
    main()
