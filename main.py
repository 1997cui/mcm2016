import roadmap
import event

global city_map
city_map = roadmap.Map(2)

def main():
    global city_map
    city_map.add_road(src=0, dst=1)
    city_map.add_road(src=1, dst=0)
    print city_map.roads
    city_map.init_queue()
    events = event.Events()
    events.push(event.WaitingStopEvent(0, 0, 0, 1))
    while True:
        events.pop()()

if __name__ == "__main__":
    main()
