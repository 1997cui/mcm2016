from main import city_map
import math
import heapq

react_min_time = 3.

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
        city_map.events.push(WaitingStartEvent(
            self.time_stamp + float(length) / min(speed_max,
                math.sqrt(2.*length/car_num/react_min_time**2.*width)
            )
            self.car_index,
            self.road_index
        ))
        next_car_index = city_map.roads[src_road_index].dequeue(road_index)
        city_map.events.push(WaitingStopEvent(
            self.time_stamp + city_map.roads[src_road_index].queues[road_index].delta_time,
            next_car_index,
            src_road_index,
            city_map.cars[next_car].next_road(),
        ))

class Events():
    def __init__(self):
        self.events=[]
    def push(self.to_push)
        heapq.heappush(self.events,to_push)
    def pop(self):
        return heapq.heappop(self.events)

