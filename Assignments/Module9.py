import random
#Module9
#Exercise1
class Car:
    def __init__(self, registration_num, max_speed):
        self.registration_num = registration_num
        self.max_speed = max_speed
        self.current_speed = 0
        self.travelled_distance=0

new_car= Car("ABC-123", 142)
print(f"Registration Number: {new_car.registration_num}")
print(f"Max Speed: {new_car.max_speed}")
print(f"Current Speed: {new_car.current_speed}")
print(f"Travelled Distance: {new_car.travelled_distance}")

#Exercise2
class Car:
    def __init__(self, registration_num, max_speed):
        self.registration_num = registration_num
        self.max_speed = max_speed
        self.current_speed = 0
        self.travelled_distance=0
    def accelerate(self,change_of_speed):
        self.current_speed += change_of_speed
        if self.current_speed > self.max_speed:
            self.current_speed = self.max_speed
        elif self.current_speed < 0:
            self.current_speed = 0

new_car= Car("ABC-123", 142)
new_car.accelerate(30)
new_car.accelerate(70)
new_car.accelerate(50)
print(f"Current speed is {new_car.current_speed}km/h")
new_car.accelerate(-200)
print(f"Final speed is {new_car.current_speed}km/h")

#Exercise3
class Car:
    def __init__(self, registration_num, max_speed):
        self.registration_num = registration_num
        self.max_speed = max_speed
        self.current_speed = 0
        self.travelled_distance=0
    def accelerate(self,change_of_speed):
        self.current_speed += change_of_speed
        if self.current_speed > self.max_speed:
            self.current_speed = self.max_speed
        elif self.current_speed < 0:
            self.current_speed = 0
    def drive(self,hours):
        distance= self.current_speed*hours
        self.travelled_distance+=distance
        print(f"The total distance travelled is {self.travelled_distance} km.")

new_car= Car("ABC-123", 142)
new_car.travelled_distance=2000
new_car.accelerate(60)
print(f"Current speed is {new_car.current_speed}km/h")
new_car.drive(1.5)
new_car.accelerate(-200)
print(f"Final speed is {new_car.current_speed}km/h")

#Exercise4
class Car:
    def __init__(self, registration_num, max_speed):
        self.registration_num = registration_num
        self.max_speed = max_speed
        self.current_speed = 0
        self.travelled_distance = 0
    def accelerate(self,change_of_speed):
        self.current_speed += change_of_speed
        if self.current_speed > self.max_speed:
            self.current_speed = self.max_speed
        elif self.current_speed < 0:
            self.current_speed = 0
    def drive(self,hours):
        distance= self.current_speed*hours
        self.travelled_distance+=distance
cars_list=[]
for i in range(1,11):
    registration_number= f"ABC-{i}"
    max_speed= random.randint(100,200)
    car= Car(registration_number, max_speed)
    cars_list.append(car)

race_finished= False
while not race_finished:
    for car in cars_list:
        change_of_speed=random.randint(-10,15)
        car.accelerate(change_of_speed)
        car.drive(1)
        if car.travelled_distance>=10000:
            race_finished=True
            break
print(f"{"Registration Number":<20} {"Maximum Speed":<16} {"Current Speed":<15} {"Travelled Distance":<20}")
for car in cars_list:
    print(f"{car.registration_num:<20} {car.max_speed:<16} {car.current_speed:<15} {car.travelled_distance:<20}")