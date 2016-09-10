from city_map import city_map

class WaitingStartEvent():
    def __init__(self,time_stamp,car_index,road_index):
        self.time_stamp = time_stamp
        self.car_index = car_index
        self.road_index = road_index
    def __cmp__(self,other):
        return self.time_stamp < other.time_stamp
    def __call__(self):
        next_road = city_map.cars[car_index].next_road()
        city_map.roads[road_index].inqueue(next_road)
        city_map.roads[road_index].car_number -= 1

class WaitingStopEvent():
    def __init__(self,time_stamp,car_index,road_index):
        self.time_stamp = time_stamp
        self.car_index = car_index
        self.road_index = road_index
    def __call__(self):
        city_map.roads[road_index].car_number += 1
        city_map.events.push(WaitingStartEvent(
            self.time_stamp + ,
            self.car_index,
            self.road_index
        ))
