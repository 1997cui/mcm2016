#!/usr/bin/env python
# -*- coding:utf-8 -*--

import heapq
import math
import os
import time

try:
    DEBUG = int(os.getenv("DEBUG"))
except TypeError:
    DEBUG = 0
except ValueError:
    DEBUG = 1


class Queue():
    def __init__(self, src, dst, k):
        self.src = int(src)
        self.dst = int(dst)
        self.queue = []
        self.k = float(k)

    def pop(self):
        to_return = self.queue[0]
        self.queue = self.queue[1:]
        return to_return

    def push(self, to_push):
        self.queue.append(to_push)


class Road:
    def __init__(self, src, dst, width, length, speed_m):
        self.src = int(src)
        self.dst = int(dst)
        self.width = int(width)
        self.length = float(length)
        self.speed_m = float(speed_m)
        self.floyd_w = self.length / self.speed_m
        self.car_num = 0
        self.queues = {}

    def expect_time(self):
        try:
            speed = min(math.sqrt(2. * (
            self.length - self.car_num * city_map.car_len) / self.car_num / city_map.rct_time ** 2. * self.width),
                        self.speed_m)  # !!! 直路时间
        except ZeroDivisionError:
            speed = self.speed_m
        return float(self.length) / speed


class CityMap:
    def __init__(self, vtx_num, edg_num, edg_prp, crs_prp, rct_time, car_len):
        self.car_len = int(car_len)
        self.vtx_num = int(vtx_num)
        self.edg_num = int(edg_num)
        self.roads = []
        self.cars = []
        self.events = Events()
        self.rct_time = float(rct_time)
        self.vtx = [[[], []] for i in range(vtx_num)]
        for i in edg_prp:
            self.roads.append(Road(i[0], i[1], i[2], i[3], i[4]))
        for i, j in enumerate(self.roads):
            self.vtx[j.src][1].append(i)
            self.vtx[j.dst][0].append(i)
        for index, i in enumerate(self.roads):
            for j in self.vtx[i.dst][1]:
                i.queues[j] = Queue(index, j, crs_prp[index][j])
        self.floyd()

    def check_run_car(self):
        for i in self.cars:
            try:
                if i.path[-1] != i.dst:
                    return True
            except IndexError:
                return True
        return False

    def floyd(self):
        self.floyd_network = [[-1 for i in range(self.vtx_num)] for j in range(self.vtx_num)]
        for i in range(self.vtx_num):
            self.floyd_network[i][i] = 0
        for i in self.roads:
            self.floyd_network[i.src][i.dst] = i.floyd_w
        flag = True
        while flag:
            flag = False
            for i in range(self.vtx_num):
                for j in range(self.vtx_num):
                    for k in range(self.vtx_num):
                        if self.floyd_network[i][k] != -1 and self.floyd_network[k][j] != -1:
                            if (self.floyd_network[i][j] == -1) or (
                                        self.floyd_network[i][j] > self.floyd_network[i][k] + self.floyd_network[k][j]):
                                self.floyd_network[i][j] = self.floyd_network[i][k] + self.floyd_network[k][j]
                                flag = True


class TypoEvent():
    def __cmp__(self, other):
        return self.time_stamp > other.time_stamp


class WaitingEvent(TypoEvent):
    def __init__(self, time_stamp, car_index, road_index):
        self.time_stamp = float(time_stamp)
        self.car_index = int(car_index)
        self.road_index = int(road_index)

    def __call__(self):
        if DEBUG >= 1:
            print("\033[0;31;40mWaitingEvent\t: Car %d in Road %d at %.2f\033[0m" % (
                self.car_index, self.road_index, self.time_stamp))
        next_road = city_map.cars[self.car_index].next_road(city_map.roads[self.road_index].dst, self.time_stamp)
        city_map.roads[self.road_index].car_num -= 1
        if next_road is None: return
        city_map.roads[self.road_index].queues[next_road].push(self.car_index)


class MovingEvent(TypoEvent):
    def __init__(self, time_stamp, car_index, src_road_index, road_index):
        self.time_stamp = float(time_stamp)
        self.car_index = int(car_index)
        self.src_road_index = int(src_road_index)
        self.road_index = int(road_index)

    def __call__(self):
        if DEBUG >= 1:
            print("\033[0;32;40mMovingEvent\t: Car %d from Road %d to Road %d at %.2f\033[0m" % (
                self.car_index, self.src_road_index, self.road_index, self.time_stamp))
        city_map.roads[self.road_index].car_num += 1
        city_map.events.push(WaitingEvent(
            self.time_stamp + city_map.roads[self.road_index].expect_time(),
            self.car_index,
            self.road_index
        ))


class StartEvent(TypoEvent):
    def __init__(self, time_stamp, car_index):
        self.time_stamp = float(time_stamp)
        self.car_index = int(car_index)

    def __call__(self):
        if DEBUG >= 1:
            print("\033[0;38;40mStartEvent\t: Car %d start at %.2f\033[0m" % (
                self.car_index, self.time_stamp))
        temp = city_map.cars[self.car_index]
        city_map.events.push(MovingEvent(temp.startime, temp.ind, -1, temp.next_road(temp.src, temp.startime)))

class CheckEvent(TypoEvent):
    def __init__(self, time_stamp, src_road_index, road_index):
        self.time_stamp = float(time_stamp)
        self.src_road_index = int(src_road_index)
        self.road_index = int(road_index)

    def __call__(self):
        if DEBUG >= 1:
            print("\033[0;34;40mCheckEvent\t: From Road %d tp Road %d at %.2f\033[0m" % (
                self.src_road_index, self.road_index, self.time_stamp))
        try:
            next_car_index = city_map.roads[self.src_road_index].queues[self.road_index].pop()
            city_map.events.push(MovingEvent(
                self.time_stamp,
                next_car_index,
                self.src_road_index,
                self.road_index,
            ))
        except IndexError:
            pass
        city_map.events.push(CheckEvent(
            self.time_stamp + city_map.roads[self.src_road_index].queues[self.road_index].k,  # !!! 路口等待时间
            self.src_road_index,
            self.road_index
        ))


class Events():
    def __init__(self):
        self.events = []

    def push(self, to_push):
        heapq.heappush(self.events, to_push)

    def pop(self):
        return heapq.heappop(self.events)

    def __str__(self):
        to_print = "\033[0;33;40mCurrent Event Queue : \033[0m"
        for i in self.events:
            color = "\033[0m"
            if isinstance(i, WaitingEvent): color = "\033[0;31;40m"
            if isinstance(i, MovingEvent): color = "\033[0;32;40m"
            if isinstance(i, CheckEvent): color = "\033[0;34;40m"
            to_print += "%s%.2f%s" % (color, i.time_stamp, " \033[0m")
        return to_print


class Car:
    def __init__(self, ind, startime, src, dst):
        self.ind = int(ind)
        self.startime = float(startime)
        self.src = int(src)
        self.dst = int(dst)
        self.path = []

    def next_road(self, crrt_vtx, time_stamp):
        self.path.append(crrt_vtx)
        if int(crrt_vtx) == self.dst:
            self.endtime = float(time_stamp)
            print("\033[0;36;40mDST \t\t: Car %d from %d(%.2f) to %d(%.2f)\033[0m\n\
\033[0;36;40mpath : %s \033[0m" % (
                self.ind, self.src, self.startime, self.dst, self.endtime, self.path))
            return None
        outer_road = city_map.vtx[crrt_vtx][1]  # !!! 这里的老司机分两种，知道大路/小路 知道堵/不堵 待完善
        expect1 = [city_map.floyd_network[city_map.roads[i].dst][self.dst] for i in outer_road]
        expect2 = [city_map.roads[i].expect_time() for i in outer_road]
        index = reduce(
            lambda x, y: x if (expect1[y] == -1) or (expect1[x] + expect2[x] < expect1[y] + expect2[y]) else y,
            range(len(outer_road)))
        return outer_road[index]

    def __call__(self):
        city_map.events.push(StartEvent(self.startime, self.ind))


def main():
    global city_map
    city_map = CityMap(6, 14, [
        [0,1,3,173,11.11],
        [1,0,3,173,11.11],
        [0,4,2,321,8.33],
        [4,0,2,321,8.33],
        [4,5,2,66,8.33],
        [5,4,2,66,8.33],
        [5,2,2,182,8.33],
        [2,5,2,182,8.33],
        [4,3,1,182,8.33],
        [3,4,1,182,8.33],
        [3,2,2,78,8.33],
        [2,3,2,78,8.33],
        [1,3,2,293,8.33],
        [3,1,2,293,8.33]
    ],[{12:45,1:60},
       {2:15,0:60},
       {3:30,4:30,8:15},
       {0:60,2:45},
       {5:30,6:15},
       {4:30,3:30,8:60},
       {7:30,11:15},
       {6:30,5:60},
       {9:30,10:60,13:15},
       {8:60,3:60,4:15},
       {7:60,11:30},
       {10:30,9:15,12:30},
       {9:60,13:30},
       {12:30,1:15}], 3.0, 4.3)
    for i in range(100):
        city_map.cars.append(Car(i, i, 2, 0))
    for i in city_map.cars:
        i()
    for index, i in enumerate(city_map.roads):
        for j in i.queues.keys():
            city_map.events.push(CheckEvent(0, index, j))
    while city_map.check_run_car():
        #if DEBUG >= 1:
        #    time.sleep(0.01)
        if DEBUG >= 2:
            print city_map.events
        city_map.events.pop()()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\033[1;30;47mInterrupted\033[0m")
