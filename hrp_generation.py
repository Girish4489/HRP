import pandas as pd
import numpy as np

# Set the random seed for reproducibility
np.random.seed(42)

# Define the number of data points to generate
num_data_points = 6000

# Define the mean and standard deviation for the size of the house
size_mean = 350
size_std = 150

# Define the location options
locations = [
    "Electronic City",
    "Silk Board",
    "Yelahanka",
    "Kengeri",
    "Majestic",
    "K.R Puram",
]

# Define the rent ranges for each location
rent_ranges = {
    "Electronic City": (15000, 35000),
    "Silk Board": (20000, 40000),
    "Yelahanka": (12000, 30000),
    "Kengeri": (10000, 25000),
    "Majestic": (18000, 38000),
    "K.R Puram": (16000, 32000),
}

# Define the range for the distance from junction in meters
junction_dist_min = 0
junction_dist_max = 10000

# Define the range for the number of rooms
num_rooms_min = 1
num_rooms_max = 5

# Define the range for the distance from metro in meters
metro_dist_min = 0
metro_dist_max = 5000

# Define the furnished options
furnished_options = ["Furnished", "Semi-furnished", "Not furnished"]
rent_adjustments = [
    20,
    10,
    0,
]  # Higher adjustment for Furnished, lower for Semi-furnished, no adjustment for Not furnished

# Define the parking options
parking_options = ["Yes", "No"]

# Define the water & electricity options
water_electricity_options = ["Yes", "No"]


def generate_data():
    # Generate the data
    data = {
        "Location": np.random.choice(locations, num_data_points),
        "Distance from Junction": np.random.uniform(
            junction_dist_min, junction_dist_max, num_data_points
        ),
        "Size of House": np.random.normal(size_mean, size_std, num_data_points).astype(
            int
        ),
        "Number of Rooms": np.random.randint(
            num_rooms_min, num_rooms_max + 1, num_data_points
        ),
        "Distance from Metro": np.random.uniform(
            metro_dist_min, metro_dist_max, num_data_points
        ),
        "Furnished": np.random.choice(
            furnished_options, num_data_points, p=[0.8, 0.1, 0.1]
        ),
        "Parking": np.random.choice(parking_options, num_data_points, p=[0.8, 0.2]),
        "Water & Electricity": np.random.choice(
            water_electricity_options, num_data_points, p=[0.8, 0.2]
        ),
    }

    # Ensure the minimum house size is 200 square feet
    data["Size of House"] = np.maximum(data["Size of House"], 200)

    # Assign rent based on location, size of the house, availability of water & electricity, parking, and furnishing
    data["Rent"] = [
        np.random.randint(low, high)
        + (size // 100)
        - (10 if water_electricity == "No" else 0)
        - (10 if parking == "No" else 0)
        + rent_adjustments[furnished_options.index(furnished)]
        + (size // 100) * (rooms * 10)
        - (distance // 100) * 10
        for location, size, water_electricity, parking, furnished, rooms, distance in zip(
            data["Location"],
            data["Size of House"],
            data["Water & Electricity"],
            data["Parking"],
            data["Furnished"],
            data["Number of Rooms"],
            data["Distance from Junction"],
        )
        for low, high in [rent_ranges[location]]
    ]

    # Create a DataFrame from the generated data
    df = pd.DataFrame(data)

    # Save the data to a CSV file
    df.to_csv("home_rent_data.csv", index=False)
