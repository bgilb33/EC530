# Geo Matching API

## Overview

This project provides a simple API that matches each point from one array of GPS locations to the closest point in another array using the Haversine formula.

## How to Start the Flask Server

1. Install dependencies if not already installed:
   ```bash
   pip install flask
   ```
2. Run the server:
   ```bash
   python script.py
   ```
   The server will start on `http://127.0.0.1:5000/`.

## How to Call the API

You can send a `POST` request to the `/match` endpoint with JSON data. Example request using `curl`:

```bash
curl -X POST http://127.0.0.1:5000/match -H "Content-Type: application/json" -d '{
    "array1": [[40.7128, -74.0060], [34.0522, -118.2437]],
    "array2": [[51.5074, -0.1278], [41.8781, -87.6298]]
}'
```

### Expected Output

The response is a JSON array where each entry consists of a point from `array1` and its closest matching point from `array2`. Example output:

```json
[
    [[40.7128, -74.006], [41.8781, -87.6298]],
    [[34.0522, -118.2437], [41.8781, -87.6298]]
]
```

This output means:

- The closest point to `(40.7128, -74.0060)` (New York City) is `(41.8781, -87.6298)` (Chicago).
- The closest point to `(34.0522, -118.2437)` (Los Angeles) is also `(41.8781, -87.6298)` (Chicago).

## Running Unit Tests

To run the tests:

```bash
pytest script.py
```

This will validate the correct implementation of the distance calculation and matching logic.


