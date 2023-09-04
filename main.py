import tkinter as tk
from tkinter import ttk
from hrp_generation import generate_data
from hrp_model import train_model, load_model, predict_rent

# Create the main window
window = tk.Tk()
window.title("House Rent Prediction")

# Define the UI components
result_label = ttk.Label(window, text="")
location_label = ttk.Label(window, text="Location:")
location_combobox = ttk.Combobox(
    window,
    values=[
        "Electronic city",
        "Silk board",
        "Yelanka",
        "Kengan",
        "Majestic",
        "K.R. Puram",
    ],
)
distance_label = ttk.Label(window, text="Distance from Junction (km):")
distance_entry = ttk.Entry(window)
size_label = ttk.Label(window, text="House Size (sqft):")
size_entry = ttk.Entry(window)
rooms_label = ttk.Label(window, text="Number of Rooms:")
rooms_combobox = ttk.Combobox(window, values=["1", "2", "3", "4", "5"])
furnished_label = ttk.Label(window, text="Furnished:")
furnished_combobox = ttk.Combobox(
    window, values=["Furnished", "Semi-furnished", "Not furnished"]
)
parking_label = ttk.Label(window, text="Parking:")
parking_combobox = ttk.Combobox(window, values=["Yes", "No"])
water_electricity_label = ttk.Label(window, text="Water/Electricity:")
water_electricity_combobox = ttk.Combobox(window, values=["Yes", "No"])


def generate_data_button_click():
    generate_data()
    result_label["text"] = "Data generated successfully"


def predict_button_click():
    location = location_combobox.get()
    junction_dist = float(distance_entry.get())
    house_size = float(size_entry.get())
    num_rooms = int(rooms_combobox.get())
    furnished = furnished_combobox.get()
    parking = parking_combobox.get()
    water_electricity = water_electricity_combobox.get()

    predicted_rent = predict_rent(
        model,
        ct,
        location,
        junction_dist,
        house_size,
        num_rooms,
        furnished,
        parking,
        water_electricity,
    )
    result_label["text"] = f"Predicted Rent: {predicted_rent}"


# Generate data if needed
generate_data_button = ttk.Button(
    window, text="Generate Data", command=generate_data_button_click
)

# Train the model if needed and load the pre-trained model and column transformer
train_model()  # Train the model and save it as a file
model, ct = load_model()  # Load the pre-trained model and column transformer

# Create the UI layout
location_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
location_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")
distance_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
distance_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
size_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
size_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
rooms_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
rooms_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")
furnished_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
furnished_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="w")
parking_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
parking_combobox.grid(row=5, column=1, padx=10, pady=5, sticky="w")
water_electricity_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
water_electricity_combobox.grid(row=6, column=1, padx=10, pady=5, sticky="w")

generate_data_button.grid(row=7, column=0, padx=10, pady=10)
predict_button = ttk.Button(window, text="Predict Rent", command=predict_button_click)
predict_button.grid(row=7, column=1, padx=10, pady=10)

result_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

window.mainloop()
