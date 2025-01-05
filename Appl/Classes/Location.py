"""
Loaction Class
Dave Exinor
Jan 5, 2024

Keeps track of the longitudinal and latitudinal coordinates of user.
"""

class Location:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    def __str__(self):
        return f"Longitude: {self.longitude}, Latitude: {self.latitude}"
    
    def getLatitude(self):
        return self.latitude
    
    def getLongitude(self):
        return self.longitude