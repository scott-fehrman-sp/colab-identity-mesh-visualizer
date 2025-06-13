import csv
import os
from typing import Dict, Tuple
from geopy.geocoders import Nominatim
from geopy.location import Location

class CoordinatesManager:
    """
    Manages city coordinates by reading from and writing to a CSV file.
    
    This class provides functionality to read city coordinates from a CSV file,
    store them in a dictionary, and write the data back to the file when changes are made.
    """
    data: Dict[str, Tuple[float, float]]

    def __init__(self, csv_file='coordinates.csv'):
        """
        Initialize the CityCoordinatesManager with a CSV file for storing city coordinates.
        
        Args:
            csv_file (str): The path to the CSV file containing city coordinates.
        """

        self.csv_file = csv_file
        self.data = {}
        self.geolocator = Nominatim(user_agent="city_coordinates_manager")
        self._read_csv()

    def _read_csv(self):
        """Read existing CSV data into the class."""
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    city_key = f"{row['city']}".lower()
                    self.data[city_key] = (float(row['latitude']), float(row['longitude']))

    def _write_csv(self):
        """Write the current data dictionary back to the CSV file."""
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['city','latitude','longitude'])
            writer.writeheader()
            for key, (latitude, longitude) in self.data.items():
                city = key
                writer.writerow({'city': city, 'latitude': latitude, 'longitude': longitude})

    def _fetch_coordinates(self, city):
        """Fetch coordinates from an online geocoding service."""
        location = None
        for attempt in range(10):
            if attempt > 0:
                print(f"... Notice: Retry {attempt} to fetch coordinates for {city} ...")
            try:
                location = self.geolocator.geocode(city)
                if location:
                    break
            except Exception:
                if attempt == 9:
                    raise ValueError(f"... Warning: Could not fetch coordinates for {city} after 10 attempts ...")
        if location and isinstance(location, Location):
            return location.latitude, location.longitude
        else:
            raise ValueError(f"... Warning: Coordinates for {city}, could not be found ...")

    def get(self, city) -> Tuple[float, float]:
        """
        Get coordinates for a city.
        If not found in local data, fetch from an online service and save.
        """
        coordinates: Tuple[float, float]

        city_key = f"{city}".lower()
        if city_key in self.data:
            return self.data[city_key]
        else:
            coordinates = self._fetch_coordinates(city)
            self.data[city_key] = coordinates
            self._write_csv()
            return coordinates

def test_coordinates_manager():
    """
    Test the CoordinatesManager class by fetching
    """
    mgr = CoordinatesManager()
    cities = [
        "Amsterdam",
        "Antwerp",
        "Athens",
        "Atlanta",
        "Austin",
        "Baltimore",
        "Bangkok",
        "Beijing",
        "Bend",
        "Berlin",
        "Boston",
        "Brasilia",
        "Bristol",
        "Brussels",
        "Charlotte",
        "Chicago",
        "Columbus",
        "Copenhagen",
        "Dallas",
        "Denver",
        "Detroit",
        "Dubai",
        "Dublin",
        "Fort Worth",
        "Hamburg",
        "Helsinki",
        "Hokkaido",
        "Hong Kong",
        "Houston",
        "Indianapolis",
        "Istanbul",
        "Jacksonville",
        "Kuala Lumpur",
        "Lisbon",
        "London",
        "Los Angeles",
        "Madrid",
        "Manila",
        "Melbourne",
        "Miami",
        "Minneapolis",
        "Montreal",
        "Moscow",
        "New York",
        "Orlando",
        "Oslo",
        "Paris",
        "Philadelphia",
        "Phoenix",
        "Rome",
        "San Antonio",
        "San Diego",
        "San Francisco",
        "San Jose",
        "Seattle",
        "Seoul",
        "Singapore",
        "Stockholm",
        "Sydney",
        "Taipei",
        "Tokyo",
        "Toronto",
        "Vancouver",
        "Vienna",
        "Washington",
        "Wilmington",
        "Zurich",
    ]

    for city in cities:
        try:
            lat, lon = mgr.get(city)
            print(f"Coordinates for {city}: {lat}, {lon}")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    test_coordinates_manager()