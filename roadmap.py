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

    def dequeue(self, next_road_index):
        for queue in self.queues:
            if queue[0] == next_road_index:
                return queue[1].pop(0)



class Map:
    def __init__(self, n=10):
        self.__fist_road_of_cross = [None] * n
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
                    self.roads[j].queue.append((k, [], 1))
                    k = self.roads[k].next
                j = self.roads[j].next
