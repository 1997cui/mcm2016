import math
import heapq

class Queue():
    def __init__(self,src,dst,k):
        self.src   = src
        self.dst   = dst
        self.queue = []
        self.k     = k
    def pop(self):
        self.queue.pop()
    def push(self, to_push):
        self.queue.push(to_push)

class Road:
    def __init__(self, src, dst, width, length, speed):
        self.src     = src
        self.dst     = dst
        self.width   = width
        self.length  = length
        self.speed   = speed
        self.car_num = 0
        self.queue   = {}

class CityMap:
    def __init__(self,vtx_num,edg_num,edg_prp,crs_prp):
        self.vtx_num = vtx_num
        self.edg_num = edg_num
        self.edg     = []
        self.cars    = []
        self.events  = []
        for i in edg_prp:
            self.edg.push(Road(i[0],i[1],i[2],i[3],i[4]))
        self.vtx     = [[[],[]] for i in xrange(vtx_num)]
        for i,j in enumerate(self.edg):
            self.vtx[j.src][1].append(i)
            self.vtx[j.dst][0].append(i)
        for i in self.edg:
            for j in self.vtx[self.edg.dst][1]:
                i.queue[j]=[]

class WaitingStartEvent():
    def __init__(self,time_stamp,car_index,road_index):
        self.time_stamp = time_stamp
        self.car_index  = car_index
        self.road_index = road_index
    def __cmp__(self,other):
        return self.time_stamp < other.time_stamp
    def __call__(self):
        next_road = city_map.cars[self.car_index].next_road()
        city_map.roads[self.road_index].enqueue(next_road,car_index)
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
        city_map.roads[self.road_index].car_num += 1
        length     = city_map.roads[self.road_index].length
        speed_max  = city_map.roads[self.road_index].speed
        car_num    = city_map.roads[self.road_index].car_num
        width      = city_map.roads[self.road_index].width
        try:
            speed  = min(math.sqrt(2.*length/car_num/react_min_time**2.*width), speed_max)
        except:
            speed  = speed_max
        events.push(WaitingStartEvent(
            self.time_stamp + float(length) / speed,
            self.car_index,
            self.road_index
        ))
        events.push(CheckEvent(
            self.time_stamp + city_map.roads[self.src_road_index].find_next_road(self.road_index)[2],
            self.src_road_index,
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
        next_car_index = city_map.roads[self.src_road_index].dequeue(self.road_index)
        events.push(WaitingStopEvent(
            self.time_stamp,
            next_car_index,
            src_road_index,
            city_map.cars[next_car].next_road(),
        ))


class Events():
    def __init__(self):
        self.events=[]
    def push(self,to_push):
        heapq.heappush(self.events,to_push)
    def pop(self):
        return heapq.heappop(self.events)


class Car:
    def __init__(self,startime_,drivingtime=0,car_index,destination,currentroad,currentqueue=0,drivingdist=0):
        self.startime =startime
        self.src      = src
        self.dest     = dest



city_map = Map(2)
events = Events()

def main():
    global city_map
    global events
    city_map.add_road(src=0, dst=1,width=1)
    city_map.add_road(src=1, dst=0,width=1)
    city_map.init_queue()
    events.push(WaitingStopEvent(0, 0, 0, 1))
    events.push(WaitingStopEvent(0, 0, 0, 1))
    while True:
        events.pop()()
if __name__ == "__main__":
    main()
