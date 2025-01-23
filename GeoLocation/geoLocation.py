import math
from typing import List, Tuple

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:

    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def match_closest_points(array1: List[Tuple[float, float]], array2: List[Tuple[float, float]]) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:

    matched_points = []
    for point1 in array1:
        closest_point = min(array2, key=lambda point2: haversine_distance(point1[0], point1[1], point2[0], point2[1]))
        matched_points.append((point1, closest_point))
    return matched_points

# Tests
import pytest

def test_haversine_distance():
    # Distance between New York City and London
    nyc = (40.7128, -74.0060)
    london = (51.5074, -0.1278)
    distance = haversine_distance(nyc[0], nyc[1], london[0], london[1])
    assert round(distance, 1) == 5570.2  # Expected ~5570.2 km

def test_match_closest_points():
    array1 = [(40.7128, -74.0060), (34.0522, -118.2437)]  # NYC, LA
    array2 = [(51.5074, -0.1278), (41.8781, -87.6298)]    # London, Chicago

    matches = match_closest_points(array1, array2)

    assert matches[0] == ((40.7128, -74.0060), (41.8781, -87.6298))  # NYC -> Chicago
    assert matches[1] == ((34.0522, -118.2437), (41.8781, -87.6298))  # LA -> Chicago

if __name__ == "__main__":
    pytest.main()