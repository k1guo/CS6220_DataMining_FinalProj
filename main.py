import pandas as pd
import numpy as np

# Define the number of data points
num_rows = 150000

# Generate latitude and longitude within Silicon Valley (approximate bounds)
latitude = np.random.uniform(37.2, 37.5, num_rows)
longitude = np.random.uniform(-122.3, -121.8, num_rows)

# Generate population density between a reasonable range
population_density = np.random.uniform(1000, 15000, num_rows)

# Generate traffic flow between a reasonable range
traffic_flow = np.random.uniform(500, 5000, num_rows)

# Generate stop point demand (binary 0 or 1)
stop_point_demand = np.random.choice([0, 1], size=num_rows, p=[0.7, 0.3])

# Generate cluster labels
cluster_label = np.random.randint(1, 11, num_rows)

# Generate existing stops, leaving 70% of them empty
existing_stops = [
    (np.random.uniform(37.2, 37.5), np.random.uniform(-122.3, -121.8))
    if np.random.rand() > 0.7 else None for _ in range(num_rows)
]

# Generate stop capacities
stop_capacity = np.random.uniform(1000, 10000, num_rows)

# Create the dataset
data = pd.DataFrame({
    "Latitude": latitude,
    "Longitude": longitude,
    "Population Density": population_density,
    "Traffic Flow": traffic_flow,
    "Stop Point Demand": stop_point_demand,
    "Cluster Label": cluster_label,
    "Existing Stops": existing_stops,
    "Stop Capacity": stop_capacity
})

# Save the data to a CSV file
data.to_csv('silicon_valley_stop_points.csv', index=False)

