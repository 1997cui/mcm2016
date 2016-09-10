class Road:
    def __init__(self, src=0, dst=0, crowd=0, length=1000, speed=10):
        self.next = -1
        self.src = src
        self.dst = dst
        self.crowd = crowd
        self.length = length
        self.speed = speed
        self.car_num = 0
        self.queue = [[], ]


class Map:
    def __init__(self, n=10):
        self.__roads__ = [None] * n
        self.__crosses__ = [None] * n
        self.__edge__ = []
        for i in range(0, n):
            pass

    def add_road(self, src=0, dst=0, crowd=0, length=1000, speed=10):
        self.__edge__.append(Road(src, dst, crowd, length, speed))
        self.__edge__[-1].next = self.__roads__[src]
        self.__roads__[src] = len(self.__edge__) - 1
