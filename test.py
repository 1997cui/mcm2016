import heapq
import math
import random

react_min_time = 3.0

class Queue():
    def __init__(self,src,dst,k):
        self.src   = src
        self.dst   = dst
        self.queue = []
        self.k     = k
    def pop(self):
        to_return  = self.queue[0]
        self.queue = self.queue[1:]
        return to_return
    def push(self, to_push):
        self.queue.append(to_push)

class Road:
    def __init__(self, src, dst, width, length, speed):
        self.src     = src
        self.dst     = dst
        self.width   = width
        self.length  = length
        self.speed   = speed
        self.car_num = 0
        self.queues  = {}

class CityMap:
    def __init__(self,vtx_num,edg_num,edg_prp,crs_prp):
        self.vtx_num = vtx_num
        self.edg_num = edg_num
        self.roads   = []
        self.cars    = []
        self.events  = Events()
        for i in edg_prp:
            self.roads.append(Road(i[0],i[1],i[2],i[3],i[4]))
        self.vtx = [[[], []] for i in range(vtx_num)]
        for i,j in enumerate(self.roads):
            self.vtx[j.src][1].append(i)
            self.vtx[j.dst][0].append(i)
        for index,i in enumerate(self.roads):
            for j in self.vtx[i.dst][1]:
                i.queues[j]=Queue(index,j,crs_prp[index][j])

class WaitingStartEvent():
    def __init__(self,time_stamp,car_index,road_index):
        self.time_stamp = time_stamp
        self.car_index  = car_index
        self.road_index = road_index
    def __cmp__(self,other):
        return self.time_stamp < other.time_stamp
    def __call__(self):
        next_road = city_map.cars[self.car_index].next_road(city_map.roads[self.road_index].dst)
        city_map.roads[self.road_index].queues[next_road].push(self.car_index)
        city_map.roads[self.road_index].car_num -= 1

class WaitingStopEvent():
    def __init__(self,time_stamp,car_index,src_road_index,road_index):
        self.time_stamp     = time_stamp
        self.car_index      = car_index
        self.src_road_index = src_road_index
        self.road_index     = road_index
    def __cmp__(self,other):
        return self.time_stamp < other.time_stamp
    def __call__(self):
        print("Car %d from Road %d to Road %d" % (self.car_index, self.src_road_index, self.road_index))
        city_map.roads[self.road_index].car_num += 1
        length     = city_map.roads[self.road_index].length
        speed_max  = city_map.roads[self.road_index].speed
        car_num    = city_map.roads[self.road_index].car_num
        width      = city_map.roads[self.road_index].width
        try:
            speed  = min(math.sqrt(2.*length/car_num/react_min_time**2.*width), speed_max)
        except:
            speed  = speed_max
        city_map.events.push(WaitingStartEvent(
            self.time_stamp + float(length) / speed,
            self.car_index,
            self.road_index
        ))
       
        
class CheckEvent():
    def __init__(self,time_stamp,src_road_index,road_index):
        self.time_stamp = time_stamp
        self.src_road_index = src_road_index
        self.road_index = road_index
    def __cmp__(self,other):
        return self.time_stamp < other.time_stamp
    def __call__(self):
        try:
            next_car_index = city_map.roads[self.src_road_index].queues[self.road_index].pop()
            city_map.events.push(WaitingStopEvent(
                self.time_stamp,
                next_car_index,
                self.src_road_index,
                city_map.cars[next_car_index].next_road(),
            ))
        except IndexError:
            pass
        city_map.events.push(CheckEvent(
            self.time_stamp + city_map.roads[self.src_road_index].queues[self.road_index].k,
            self.src_road_index,
            self.road_index
        ))

class Events():
    def __init__(self):
        self.events=[]
    def push(self,to_push):
        heapq.heappush(self.events,to_push)
    def pop(self):
        return heapq.heappop(self.events)

class Car:
    def __init__(self,id,startime,src,dst):
        self.id       = id
        self.startime = startime
        self.src      = src
        self.dst      = dst
    def next_road(self,crrt_vtx):
        if crrt_vtx == self.dst:
            return None
        to_ran = city_map.vtx[crrt_vtx][1]
        le     = len(to_ran)
        a      = int(random.random()*le)
        return to_ran[a]
    def __call__(self):
        city_map.events.push(WaitingStopEvent(self.startime,self.id,-1,self.next_road(self.src)))

city_map = CityMap(3,2,[[0,1,1,1000,10],[1,2,1,1000,10]],[{1:10},{}])

def main():
    global city_map
    city_map.cars.append(Car(0,0,0,1))
    for i in city_map.cars:
        i()
    for index,i in enumerate(city_map.roads):
        for j in i.queues.keys():
            city_map.events.push(CheckEvent(0,index,j))
    while True:
        city_map.events.pop()()
if __name__ == "__main__":
    main()
