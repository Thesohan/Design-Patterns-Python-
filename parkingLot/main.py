import threading
import time
import heapq
import uuid

class ParkingSpot:
    def __init__(self, spot_id, level, priority, vehicle_type):
        self.spot_id = spot_id
        self.level = level
        self.priority = priority  # Lower value = higher priority
        self.vehicle_type = vehicle_type
        self.is_available = True
        self.vehicle = None

    def assign_vehicle(self, vehicle):
        self.is_available = False
        self.vehicle = vehicle

    def remove_vehicle(self):
        self.is_available = True
        self.vehicle = None

    def __lt__(self, other):
        return self.priority < other.priority  # For heap-based priority queue


class ParkingLot:
    def __init__(self):
        self.spots = []
        self.lock = threading.Lock()

    def add_spot(self, spot):
        with self.lock:
            heapq.heappush(self.spots, spot)

    def find_and_assign_spot(self, vehicle):
        with self.lock:
            for spot in self.spots:
                if spot.is_available and spot.vehicle_type == vehicle.vehicle_type:
                    spot.assign_vehicle(vehicle)
                    return spot
        return None

    def free_spot(self, spot_id):
        with self.lock:
            for spot in self.spots:
                if spot.spot_id == spot_id:
                    spot.remove_vehicle()
                    return True
        return False


class ParkingTicket:
    def __init__(self, vehicle, spot):
        self.ticket_id = uuid.uuid4()
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = time.time()

    def calculate_fee(self, exit_time):
        duration = exit_time - self.entry_time
        rate_per_hour = {"Car": 10, "Motorcycle": 5, "Truck": 20}
        return rate_per_hour[self.vehicle.vehicle_type] * (duration / 3600)


class Gate:
    def __init__(self, gate_id, parking_lot):
        self.gate_id = gate_id
        self.parking_lot = parking_lot

    def vehicle_entry(self, vehicle):
        print(f"Gate {self.gate_id}: Vehicle {vehicle.vehicle_id} trying to enter.")
        spot = self.parking_lot.find_and_assign_spot(vehicle)
        if spot:
            ticket = ParkingTicket(vehicle, spot)
            print(f"Gate {self.gate_id}: Vehicle {vehicle.vehicle_id} parked at Spot {spot.spot_id}.")
            return ticket
        else:
            print(f"Gate {self.gate_id}: No spot available for Vehicle {vehicle.vehicle_id}.")
            return None

    def vehicle_exit(self, ticket):
        print(f"Gate {self.gate_id}: Vehicle {ticket.vehicle.vehicle_id} exiting from Spot {ticket.spot.spot_id}.")
        exit_time = time.time()
        fee = ticket.calculate_fee(exit_time)
        self.parking_lot.free_spot(ticket.spot.spot_id)
        print(f"Gate {self.gate_id}: Vehicle {ticket.vehicle.vehicle_id} exited. Fee: ${fee:.2f}.")


class Vehicle:
    def __init__(self, vehicle_id, vehicle_type):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type


if __name__ == "__main__":
    # Create Parking Lot
    parking_lot = ParkingLot()

    # Add spots with custom priority
    for i in range(1, 6):
        parking_lot.add_spot(ParkingSpot(i, 1, i, "Car"))
    for i in range(6, 8):
        parking_lot.add_spot(ParkingSpot(i, 1, i, "Motorcycle"))
    for i in range(8, 10):
        parking_lot.add_spot(ParkingSpot(i, 1, i, "Truck"))

    # Create Gates
    gate1 = Gate(1, parking_lot)
    gate2 = Gate(2, parking_lot)

    # Create Vehicles
    vehicles = [
        Vehicle("123ABC", "Car"),
        Vehicle("456DEF", "Motorcycle"),
        Vehicle("789GHI", "Truck"),
        Vehicle("321JKL", "Car"),
    ]

    # Simulate entry and exit
    tickets = []
    for vehicle in vehicles:
        ticket = gate1.vehicle_entry(vehicle)
        if ticket:
            tickets.append(ticket)
            print(ticket)
        time.sleep(0.5)  # Simulate delay between arrivals

    for ticket in tickets:
        gate2.vehicle_exit(ticket)
        time.sleep(0.5)  # Simulate delay between exits
