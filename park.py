import random
import json
import boto3
from collections import Counter

class ParkingLot:
    def __init__(self, square_footage, spot_length=8, spot_width=12):
        self.square_footage = square_footage
        self.spot_size = spot_length * spot_width
        self.num_spots = int(self.square_footage / self.spot_size)
        self.spots = [None] * self.num_spots
        self.car_spot_map = {}
        

    def park(self, car, spot_num):
        if self.spots[spot_num] is None:
            self.spots[spot_num] = car
            self.car_spot_map[str(car)] = spot_num

            print(f"Car with license plate {car.license_plate} parked successfully in spot {spot_num}.")

            return True
        # else:
        #     # print(f"Spot {spot_num} is occupied. Trying to park in another spot...")
        #     return False

    def get_car_spot_map(self):
        return self.car_spot_map

    def save_car_spot_map(self, bucket_name, filename):
        s3 = boto3.client('s3')
        s3.put_object(Bucket=bucket_name, Key=filename, Body=json.dumps(self.car_spot_map))


class Car:
    def __init__(self, license_plate):
        self.license_plate = license_plate

    def __str__(self):
        return self.license_plate


def main(cars, parking_lot):
    for car in cars:
        parked = False
        while not parked:
            spot_num = random.randint(0, parking_lot.num_spots - 1)
            parked = parking_lot.park(car, spot_num)
            if not parked:
                continue
            else:
                break


if __name__ == '__main__':
    # create a parking lot with a size of 2000 square feet and spot size of 8x12
    parking_lot = ParkingLot(2000)

    # create an array of cars with random license plates
    cars = [Car(str(random.randint(1000000, 9999999))) for i in range(100)]
    

    # park the cars in the parking lot
    main(cars, parking_lot)

    # save the car-spot map to S3
    parking_lot.save_car_spot_map("my-bucket", "car_spot_map.json")
