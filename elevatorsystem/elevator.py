import time
# from threading import Lock, Condition
# from request import Request
# from direction import Direction
from direction import Direction
from threading import Lock, Condition
from request import Request
class Elevator:

    def __init__(self,id:int,capacity:int):
        self.id = id 
        self.capacity = capacity 
        self.current_floor = 1
        self.current_direction = Direction.UP
        self.requests = []
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def add_request(self, request:Request):
        with self.lock:
            if len(self.requests) < self.capacity:
                self.requests.append(request)
                print(
                    f"Elevator {self.id} added request: {request.src_floor} to {request.dst_floor}"
                )
                self.condition.notify_all()

    def get_next_request(self)->Request:
        with self.lock:
            while not self.requests:
                self.condition.wait()
            return self.requests.pop(0)


    def process_requests(self):
        while True:
            request = self.get_next_request()
            self.process_request(request)

    def process_request(self, request: Request):
        with self.lock:
            start_floor = self.current_floor
        src_floor, end_floor = request.src_floor, request.dst_floor

        # Move to source floor
        if start_floor != src_floor:
            self.__move_to_floor(start_floor, src_floor)
            print(f"Elevator {self.id}:People onboarded.....")
            time.sleep(2)

        # Move to destination floor
        if src_floor != end_floor:
            self.__move_to_floor(src_floor, end_floor)
            print(f"Elevator {self.id}: People dropped.....")
            time.sleep(2)

    def __move_to_floor(self, start: int, end: int):
        direction = Direction.UP if start < end else Direction.DOWN
        for i in range(start, end + (1 if direction == Direction.UP else -1), 1 if direction == Direction.UP else -1):
            with self.lock:
                self.current_floor = i
            print(f"Elevator {self.id} reached floor {self.current_floor}")
            time.sleep(1)

    def run(self):
        self.process_requests()