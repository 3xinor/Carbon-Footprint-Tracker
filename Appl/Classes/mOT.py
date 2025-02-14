"""
mOT Class (Mode of Transportation)
Dave Exinor
Jan 5, 2024

Identifies modes of transportation and their associated emmisions.
"""
import requests
import csv
import io

from abc import ABC, abstractmethod
from enum import Enum

class mOTType(Enum):
    CAR = 1
    BUS = 2
    TRAIN = 3
    PLANE = 4
    BIKE = 5
    WALK = 6

class mOT(ABC):
    def __init__(self, mOT_type):
        self.mOT_type = mOT_type
    
    def __str__(self):
        return f"Mode of Transportation: {self.mOT_type}"
    
    def getmOTType(self):
        return self.mOT_type
    
    @abstractmethod
    def getEmissions(self):
        pass

class Car(mOT):
    def __init__(self):
        super().__init__(mOTType.CAR)
    
    def getEmissions(self, vehicle_make, vehicle_model):
        """
        Download the CSV from Open Canada's dataset, parse it,
        and find the CO2 emissions (g/km) for the specified
        make and model.

        :param make:  e.g. "Ford"
        :param model: e.g. "Focus"
        :return: list of matching emissions results (each entry is a dict)
        """
        url = "https://open.canada.ca/data/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64/resource/edba4afa-dc19-480c-bbe4-57992fc9d0d6/download" 

        response = requests.get(url)
        response.raise_for_status()

        # read the csv data
        file_obj = io.StringIO(response.text)
        reader = csv.DictReader(file_obj)

        results = []

        for row in reader:
            # Adjust the key names below based on actual CSV headers
            row_make = row.get("Make", "").strip().lower()
            row_model = row.get("Model", "").strip().lower()

            if vehicle_make.lower() == row_make and vehicle_model.lower() == row_model:
                # Extract the CO2 emissions column
                results.append(float(row['CO2 emissions (g/km)']))
        return sum(results) / len(results) # g CO2 per km 
    
class Bus(mOT):
    def __init__(self):
        super().__init__(mOTType.BUS)
    
    def getEmissions(self):
        return 0.1 # g CO2 per km
    
class Train(mOT):
    def __init__(self):
        super().__init__(mOTType.TRAIN)
    
    def getEmissions(self):
        return 0.05 # g CO2 per km
    
class Plane(mOT):
    def __init__(self):
        super().__init__(mOTType.PLANE)
    
    def getEmissions(self):
        return 0.3 # g CO2 per km
    
class Bike(mOT):
    def __init__(self):
        super().__init__(mOTType.BIKE)
    
    def getEmissions(self):
        return 0 # g CO2 per km
    
class Walk(mOT):
    def __init__(self):
        super().__init__(mOTType.WALK)
    
    def getEmissions(self):
        return 0 # g CO2 per km
    
if __name__ == '__main__':
    test_car = Car()
    emmissions = test_car.getEmissions("Acura", "Integra A-SPEC")
    print(emmissions)