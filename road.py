class Road:
    def __init__(self, src=0, dst=0, crowd=0, length=1000, speed=10):
        self.next = None
        self.src = src
        self.dst = dst
        self.crowd = crowd
        self.length = length
        self.speed = speed
        self.car_num = 0
        self.queue = []

    def enqueue(self, ):
class Map:
    def __init__(self, n=10):
        self.roads = [None] * n
        self.crosses = [None] * n
        for i in range(0, n):
            pass

    def add_road(self, src=0, dst=0, crowd=0, length=1000, speed=10):
        t = Road(src, dst, crowd, length, speed)
        t.next = self.roads[src]
        self.roads[src] = t
