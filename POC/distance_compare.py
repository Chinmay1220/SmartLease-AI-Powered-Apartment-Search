# import requests

# # Token (mapbox)
# access_token = "sk.eyJ1IjoicHJhYW5hdiIsImEiOiJjbTN4NHF1a2YwMGt5MnZxMW5vZXlydGVoIn0.vLezPMPgm_0t6r77sAFytg"  # Replace with your actual Mapbox token

# # Function to get coordinates from location name
# def get_coordinates(location_name):
#     geocode_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location_name}.json"
#     params = {
#         "access_token": access_token,
#         "limit": 1  # Limit to the best match
#     }
#     response = requests.get(geocode_url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         if data["features"]:
#             coordinates = data["features"][0]["geometry"]["coordinates"]
#             return coordinates
#         else:
#             print(f"Location '{location_name}' not found.")
#             return None
#     else:
#         print(f"Error: {response.status_code} - {response.text}")
#         return None

# # Function to calculate distance between two coordinates
# def calculate_distance(start_coords, end_coords):
#     directions_url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}"
#     params = {
#         "access_token": access_token,
#         "geometries": "geojson",
#         "overview": "full"
#     }
#     response = requests.get(directions_url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         if data["routes"]:
#             distance_meters = data["routes"][0]["distance"]
#             distance_km = distance_meters / 1000  # Convert to kilometers
#             return distance_km
#         else:
#             print("No routes found.")
#             return None
#     else:
#         print(f"Error: {response.status_code} - {response.text}")
#         return None

# # Input locations
# locations = [
#     "24 Oyster Bay Rd Boston, MA 02125",
#     "1211 Dorchester Ave Dorchester, MA 02125",
#     "1171 Boylston Street, MA 02215",
#     "1 Infinite Loop Cupertino, CA 95014"
# ]
# target_location = "Northeastern University"

# # Get coordinates for all locations
# location_coords = [get_coordinates(location) for location in locations]
# target_coords = get_coordinates(target_location)

# # Compare distances
# if target_coords and all(location_coords):
#     closest_location = None
#     min_distance = float('inf')

#     for idx, coords in enumerate(location_coords):
#         distance = calculate_distance(coords, target_coords)
#         if distance is not None:
#             print(f"Distance from '{locations[idx]}' to '{target_location}': {distance:.2f} km")
#             if distance < min_distance:
#                 min_distance = distance
#                 closest_location = locations[idx]

#     if closest_location:
#         print(f"\nThe closest location to '{target_location}' is '{closest_location}' with a distance of {min_distance:.2f} km.")




# Direct comparison 


import requests

# Replace with your Mapbox API token
access_token = "sk.eyJ1IjoicHJhYW5hdiIsImEiOiJjbTN4NHF1a2YwMGt5MnZxMW5vZXlydGVoIn0.vLezPMPgm_0t6r77sAFytg"  # Replace with your actual Mapbox token

# Function to get coordinates from location name
def get_coordinates(location_name):
    geocode_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location_name}.json"
    params = {
        "access_token": access_token,
        "limit": 1  # Limit to the best match
    }
    response = requests.get(geocode_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["features"]:
            coordinates = data["features"][0]["geometry"]["coordinates"]
            return coordinates
        else:
            print(f"Location '{location_name}' not found.")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to calculate distance between two coordinates
def calculate_distance(start_coords, end_coords):
    directions_url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}"
    params = {
        "access_token": access_token,
        "geometries": "geojson",
        "overview": "full"
    }
    response = requests.get(directions_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["routes"]:
            distance_meters = data["routes"][0]["distance"]
            distance_km = distance_meters / 1000  # Convert to kilometers
            return distance_km
        else:
            return None
    else:
        return None

# Input locations
locations = [
    "24 Oyster Bay Rd Boston, MA 02125",
    "1211 Dorchester Ave Dorchester, MA 02125",
    "1171 Boylston Street, MA 02215",
    "1 Infinite Loop Cupertino, CA 95014"
]
target_location = "Northeastern University"

# Get coordinates for all locations
location_coords = [get_coordinates(location) for location in locations]
target_coords = get_coordinates(target_location)

# Find the closest location
if target_coords and all(location_coords):
    closest_location = None
    min_distance = float('inf')

    for idx, coords in enumerate(location_coords):
        distance = calculate_distance(coords, target_coords)
        if distance is not None and distance < min_distance:
            min_distance = distance
            closest_location = locations[idx]

    if closest_location:
        print(f"The closest location to '{target_location}' is '{closest_location}' with a distance of {min_distance:.2f} km.")
