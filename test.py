class Road:
    def __init__(self, src=0, dst=0, width=0, length=1000, speed=10):
        self.next = -1
        self.src = src
        self.dst = dst
        self.width = width
        self.length = length
        self.speed = speed
        self.car_num = 0
        self.queues = []

    def enqueue(self, next_road_index, car):
        for queue in self.queues:
            if queue[0] == next_road_index:
                queue[1].append(car)
                return
        raise KeyError("next road not found!")

    def dequeue(self, next_road_index):
        for queue in self.queues:
            if queue[0] == next_road_index:
                return queue[1].pop(0)
        raise KeyError("next road not found!")


class Map:
    def __init__(self, n=10):
        self.__fist_road_of_cross = [-1] * n
        self.__crosses = [None] * n
        self.roads = []
        self.n = n
        self.changeable = True
        for i in range(0, n):
            pass

    def add_road(self, src=0, dst=0, width=0, length=1000, speed=10):
        if not self.changeable:
            raise AttributeError("You could not change roads now!")
        self.roads.append(Road(src, dst, width, length, speed))
        self.roads[-1].next = self.__fist_road_of_cross[src]
        self.__fist_road_of_cross[src] = len(self.roads) - 1

    def init_queue(self):
        self.changeable = False
        for i in range(0, self.n):
            j = self.__fist_road_of_cross[i]
            while j != -1:
                dst = self.roads[j].dst
                k = self.__fist_road_of_cross[dst]
                while k != -1:
                    self.roads[j].queues.append((k, [], 1))
                    k = self.roads[k].next
                j = self.roads[j].next
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
        print self.road_index
        print city_map.roads
        city_map.roads[self.road_index].car_num += 1
        length     = city_map.roads[self.road_index].length
        speed_max  = city_map.roads[self.road_index].speed
        car_num    = city_map.roads[self.road_index].car_num
        width      = city_map.roads[self.road_index].width
        try:
            print speed_max
            print car_num
            print length
            print width
            print 2.*length/car_num/react_min_time**2.*width
            speed  = min(math.sqrt(2.*length/car_num/react_min_time**2.*width), speed_max)
            print speed
        except:
            print "ERROR"
            speed  = speed_max
        print speed
        events.push(WaitingStartEvent(
            self.time_stamp + float(length) / speed,
            self.car_index,
            self.road_index
        ))
        events.push(CheckEvent(
            self.time_stamp + city_map.roads[self.src_road_index].queues[self.road_index].delta_time,
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

city_map = Map(2)
events = Events()

def main():
    global city_map
    global events
    city_map.add_road(src=0, dst=1,width=1)
    city_map.add_road(src=1, dst=0,width=1)
    print city_map.roads
    city_map.init_queue()
    events.push(WaitingStopEvent(0, 0, 0, 1))
    events.push(WaitingStopEvent(0, 0, 0, 1))
    while True:
        events.pop()()

if __name__ == "__main__":
    main()
