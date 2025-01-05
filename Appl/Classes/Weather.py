"""
Weather Class
Dave Exinor
Jan 5, 2024

Keeps track of the lweather at a users location.
"""
import math
import requests
import xml.etree.ElementTree as ET

import bisect

def maintain_sorted_list(numbers):
    """
    Given an iterable of numbers, maintain a sorted list
    by inserting each number in its correct position.
    Returns the final sorted list.
    """
    sorted_list = []
    for num in numbers:
        # Insert `num` into sorted_list while maintaining sorted order
        bisect.insort(sorted_list, num)
        print(f"After inserting {num}, list is now: {sorted_list}")
    return sorted_list

# Full Canadian site list
site_list_url = "https://dd.weather.gc.ca/citypage_weather/xml/siteList.xml"

class Weather:
    def __init__(self, location):
        self.location = location # (longitude, latitude)
        self.temperature = None # Celsius
        self.humidity = None # Percentage
        self.wind_speed = None # km/h
        self.elevation = None # meters HOW TO GET ELEVATION

    def __str__(self):
        return f"Temperature: {self.temperature}, Humidity: {self.humidity}, Wind Speed: {self.wind_speed}, Location: {self.location}"
    
    def getTemperature(self):
        return self.temperature
    
    def getHumidity(self):
        return self.humidity
    
    def getWindSpeed(self):
        return self.wind_speed
    
    def getElevation(self):
        return self.elevation
    
    def getLocation(self):
        return self.location
    
    def __haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Compute haversine distance between two points on Earth (in kilometers).
        
        :param lat1: float - latitude of point 1 (degrees)
        :param lon1: float - longitude of point 1 (degrees)
        :param lat2: float - latitude of point 2 (degrees)
        :param lon2: float - longitude of point 2 (degrees)
        :return: float - distance in kilometers
        """
        # Earth’s average radius in kilometers
        R = 6371.0
        
        # Convert degrees to radians
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lambda = math.radians(lon2 - lon1)
    
        # Haversine formula
        a = (math.sin(d_phi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def __convert_coord(self, coord_str):
        # Last character indicates hemisphere/direction
        direction = coord_str[-1].upper()
        # Everything except that character is the numeric part
        numeric_part = coord_str[:-1]

        # Convert to float
        try:
            value = float(numeric_part)
        except ValueError:
            return None
        
        # Apply sign
        if direction in ['S', 'W']:
            value = -value
        # If direction is 'N' or 'E', it remains positive
        return value
    
    def findWeatherStats(self):
        """
        Fetches weather data at a given locastion from Environment Canada's citypage_weather feed

        :returns None
        """

        # find nearest city code
        try:
            response = requests.get(site_list_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error downloading siteList.xml: {e}")
            return None
        
        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as e:
            print(f"Error parsing siteList.xml: {e}")
            return None
        
        # Track the nearest site
        nearest_site = None
        nearest_distance = float('inf')

        for site in root.findall('site'): 
            site_code = site.get('code')
            province_code = site.find("provinceCode").text 

            # find nearest city code
            if province_code == "ON":
                try:
                    response_site = requests.get(f"https://dd.weather.gc.ca/citypage_weather/xml/{province_code}/{site_code}_e.xml")
                    response_site.raise_for_status()
                except requests.RequestException as e:
                    print(f"Error downloading site_e.xml: {e}")
                    return None
                
                try:
                    root_sub = ET.fromstring(response_site.content)
                except ET.ParseError as e:
                    print(f"Error parsing site_e.xml: {e}")
                    return None
                
                # 1. Extract lat/lon from the <location><name> element
                location_name_elem = root_sub.find("./location/name")
                location_lat = None
                location_lon = None

                if location_name_elem is not None:
                    lat_str = location_name_elem.get("lat")  
                    lon_str = location_name_elem.get("lon")
                else:
                    continue  # skip if no lat/lon found

                temp_lat = self.__convert_coord(lat_str)
                temp_lon = self.__convert_coord(lon_str)
                
                # Compute distance
                dist = self.__haversine_distance(self.location.getLatitude(), self.location.getLongitude(), temp_lat, temp_lon)
                
                if dist < nearest_distance:
                    nearest_distance = dist
                    nearest_site = (province_code, site_code)

        if nearest_site is None:
            print("No site found")
            return
        
        else:
            province_code, site_code = nearest_site
            weather_url = f"https://dd.weather.gc.ca/citypage_weather/xml/{province_code}/{site_code}_e.xml"

            try:
                response = requests.get(weather_url)
                response.raise_for_status()

            except requests.RequestException as e:
                print(f"Error fetching data from Environment Canada: {e}")
                return None
            try:
                root_final = ET.fromstring(response.content)
            except ET.ParseError as e:
                print(f"Error parsing Environment Canada XML: {e}")
                return None

            # Extract the desired data from the XML

            # Find text from relevant elements (or None if not found)
            temperature_str = root_final.findtext(".//currentConditions/temperature")
            humidity_str = root_final.findtext(".//currentConditions/relativeHumidity")
            wind_speed_str = root_final.findtext(".//currentConditions/wind/speed")

            try:
                self.temperature = float(temperature_str) if temperature_str else None
            except ValueError as e:
                print(f"Error parsing temperature: {e}")

            try:
                self.humidity = int(humidity_str) if humidity_str else None
            except ValueError as e:
                print(f"Error parsing humidity: {e}")

            try:
                self.wind_speed = float(wind_speed_str) if wind_speed_str else None
            except ValueError as e:
                print(f"Error parsing wind speed: {e}")
        return 
    
class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"Longitude: {self.longitude}, Latitude: {self.latitude}"
    
    def getLatitude(self):
        return self.latitude
    
    def getLongitude(self):
        return self.longitude
        



if __name__ == "__main__":
    # Test the Weather class
    loc = Location(45.4215, -75.6972)
    weather = Weather(loc)
    weather.findWeatherStats()
    print(weather)
