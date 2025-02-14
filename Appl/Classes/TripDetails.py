"""
Trip Details
Dave Exinor
Jan 5, 2024

Encompasses all of the back end logic needed to determine a user's expected CO2 emmissions for a trip.
"""
from enum import Enum
import Weather
import mOT

class Traffic(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TripDetails:
    
    def __init__(self, distance=0, mOT=None, weather=None, traffic=None):
        self.distance = distance
        self.mOT = mOT
        self.weather = weather
        self.traffic = traffic

    def __str__(self):
        return f"Distance: {self.distance}, Mode of Transportation: {self.mOT}, Weather: {self.weather}, Traffic: {self.traffic}"
    
    def getDistance(self):
        return self.distance
    
    def getmOT(self):
        return self.mOT
    
    def getWeather(self):
        return self.weather
    
    def getTraffic(self):
        return self.traffic
    
    def setDistance(self, distance):
        self.distance = distance

    def setmOT(self, mOT):
        self.mOT = mOT

    def setWeather(self, weather):
        self.weather = weather

    def setTraffic(self, traffic):
        self.traffic = traffic

    def getCO2Emissions(self):
        """
        Calculate the expected CO2 emissions for a trip.
        """
        distance * 