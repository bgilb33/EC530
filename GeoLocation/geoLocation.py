import math
from typing import List, Tuple
from flask import Flask, request, jsonify
import pytest
import tracemalloc
import cProfile

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371  # Earth's radius in kilometers
    
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def match_closest_points(array1: List[Tuple[float, float]], array2: List[Tuple[float, float]]) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    if not array2:
        raise ValueError("Second array cannot be empty")
    
    matched_points = []
    for point1 in array1:
        closest_point = min(array2, key=lambda point2: haversine_distance(point1[0], point1[1], point2[0], point2[1]))
        matched_points.append((point1, closest_point))
    return matched_points

# Flask API
app = Flask(__name__)

@app.route("/match", methods=["POST"])
def match_points_api():
    data = request.get_json()
    array1 = data.get("array1", [])
    array2 = data.get("array2", [])
    
    try:
        matched_points = match_closest_points(array1, array2)
        return jsonify(matched_points)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Performance Profiling

def profile_memory():
    """Analyze memory usage."""
    tracemalloc.start()
    snapshot = tracemalloc.take_snapshot()
    for stat in snapshot.statistics("lineno")[:10]:
        print(stat)

def profile_cpu():
    """Profile CPU usage."""
    cProfile.run('match_closest_points([(40.7128, -74.0060)], [(41.8781, -87.6298)])')

# Unit Tests
def test_haversine_distance():
    nyc = (40.7128, -74.0060)
    london = (51.5074, -0.1278)
    distance = haversine_distance(nyc[0], nyc[1], london[0], london[1])
    assert round(distance, 1) == 5570.2

def test_match_closest_points():
    array1 = [(40.7128, -74.0060), (34.0522, -118.2437)]  # NYC, LA
    array2 = [(51.5074, -0.1278), (41.8781, -87.6298)]    # London, Chicago
    matches = match_closest_points(array1, array2)
    assert matches[0] == ((40.7128, -74.0060), (41.8781, -87.6298))  # NYC -> Chicago
    assert matches[1] == ((34.0522, -118.2437), (41.8781, -87.6298))  # LA -> Chicago

def test_same_points():
    array1 = [(37.7749, -122.4194)]  # San Francisco
    array2 = [(37.7749, -122.4194)]  # San Francisco
    matches = match_closest_points(array1, array2)
    assert matches[0] == ((37.7749, -122.4194), (37.7749, -122.4194))

def test_multiple_points():
    array1 = [(48.8566, 2.3522), (52.5200, 13.4050)]  # Paris, Berlin
    array2 = [(40.7128, -74.0060), (34.0522, -118.2437), (41.8781, -87.6298)]  # NYC, LA, Chicago
    matches = match_closest_points(array1, array2)
    assert matches[0][1] in array2
    assert matches[1][1] in array2

def test_empty_array():
    array1 = [(40.7128, -74.0060)]  # NYC
    array2 = []  # No points to match to
    with pytest.raises(ValueError):
        match_closest_points(array1, array2)

if __name__ == "__main__":
    print("Profiling memory usage...")
    profile_memory()
    print("Profiling CPU usage...")
    profile_cpu()
    app.run(debug=True)
