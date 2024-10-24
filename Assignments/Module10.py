import random
#Module10
#Exercise1
class Elevator:
    def __init__(self,bottom,top):
        self.bottom_floor=bottom
        self.top_floor=top
        self.current_floor=bottom

    def go_to_floor(self,floor):
        if floor>self.top_floor or floor<self.bottom_floor:
            print("Not a valid floor")
            return
        while floor>self.current_floor:
            self.floor_up()
        while floor<self.current_floor:
            self.floor_down()
    def floor_up(self):
        self.current_floor+=1
        print(f"The elevator is at floor {self.current_floor} now.")
    def floor_down(self):
        self.current_floor-=1
        print(f"The elevator is at floor {self.current_floor} now.")

elevator1= Elevator (1,9)
target_floor= int(input("Enter the floor you want to go to: "))
elevator1.go_to_floor(target_floor)

#Exercise2and3:
class Elevator:
    def __init__(self,bottom,top):
        self.bottom_floor=bottom
        self.top_floor=top
        self.current_floor=bottom

    def go_to_floor(self,floor):
        if floor>self.top_floor or floor<self.bottom_floor:
            print("Not a valid floor")
            return
        while floor>self.current_floor:
            self.floor_up()
        while floor<self.current_floor:
            self.floor_down()
    def floor_up(self):
        self.current_floor+=1
        print(f"The elevator is at floor {self.current_floor} now.")
    def floor_down(self):
        self.current_floor-=1
        print(f"The elevator is at floor {self.current_floor} now.")

class Building:
    def __init__(self,bottom,top, num):
        self.bottom_floor=bottom
        self.top_floor=top
        self.num_of_elevators=num
        self.elevators= []
        for i in range(num):
            self.elevators.append(Elevator(bottom,top))

    def run_elevator(self, elevator_num, floor):
        print(f"Elevator {elevator_num} is moving.")
        self.elevators[elevator_num-1].go_to_floor(floor)

    def fire_alarm(self):
        print("Fire alarm is ringing.")
        for elevator in self.elevators:
            elevator.go_to_floor(elevator.bottom_floor)

print("\nElevators: ")
building1= Building(1,7,5)
building1.run_elevator(1,5)
building1.fire_alarm()
#Exercise4
from Module9 import Car

class Race:
    def __init__(self,name,distance,cars):
        self.name=name
        self.distance=distance
        self.cars=cars
    def hour_passes(self):
        for car in self.cars:
            car.accelerate(random.randint(-10,15))
            car.drive(1)

    def print_status(self):
        print(f"{self.name}:")
        print(f"Status after {hours} hours.")
        print(f"{"Registration Number":<20} {"Maximum Speed":<16} {"Current Speed":<15} {"Travelled Distance":<20}")
        for car in self.cars:
            print(f"{car.registration_num:<20} {car.max_speed:<16} {car.current_speed:<15} {car.travelled_distance:<20}")

    def race_finished(self):
        for car in self.cars:
            if car.travelled_distance >= self.distance:
                return True
        return False

cars_list=[]
for i in range(1,11):
    registration_number= f"ABC-{i}"
    max_speed= random.randint(100,200)
    car= Car(registration_number, max_speed)
    cars_list.append(car)
race= Race("Grand Demoliton Derby", 8000, cars_list)
hours=0
while not race.race_finished():
    race.hour_passes()
    hours+=1
    if hours %10==0:
        race.print_status()

race.print_status()





