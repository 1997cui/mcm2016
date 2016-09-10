from city_map import city_map
import math

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
        city_map.roads[self.road_index].inqueue(next_road)
        city_map.roads[self.road_index].car_number -= 1

class WaitingStopEvent():
    def __init__(self,time_stamp,car_index,road_index):
        self.time_stamp = time_stamp
        self.car_index = car_index
        self.road_index = road_index
    def __call__(self):
        city_map.roads[self.road_index].car_number += 1
        length     = city_map.roads[self.road_index].length
        speed_max  = city_map.roads[self.road_index].speed_max
        car_number = city_map.roads[self.road_index].car_number
        width      = city_map.roads[self.road_index].width
        city_map.events.push(WaitingStartEvent(
            self.time_stamp + float(length) / min(speed_max,
                math.sqrt(2.*length/car_number/react_min_time**2.*width)
            )
            self.car_index,
            self.road_index
        ))
