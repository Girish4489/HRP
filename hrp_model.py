import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import joblib


# Function to train the model and save it as a file
def train_model():
    # Load the data from the CSV file
    data = pd.read_csv("home_rent_data.csv")

    # Split the data into features (X) and target variable (y)
    X = data.drop("Rent", axis=1)
    y = data["Rent"]

    # Split the data into training and testing sets (40% train, 60% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.6, random_state=42
    )

    # Perform encoding for categorical variables
    ct = ColumnTransformer(
        transformers=[
            ("encoder_location", OneHotEncoder(handle_unknown="ignore"), ["Location"]),
            ("encoder_furnished", OrdinalEncoder(), ["Furnished"]),
            ("encoder_parking", OrdinalEncoder(), ["Parking"]),
            ("encoder_water_electricity", OrdinalEncoder(), ["Water & Electricity"]),
        ],
        remainder="passthrough",
    )

    X_train = ct.fit_transform(X_train)
    X_test = ct.transform(X_test)

    # Create the linear regression model
    model = LinearRegression()

    # Fit the model to the training data
    model.fit(X_train, y_train)

    # Save the trained model as a file
    joblib.dump(model, "hrp_model.joblib")
    joblib.dump(ct, "column_transformer.joblib")


# Function to load the trained model and column transformer
def load_model():
    model = joblib.load("hrp_model.joblib")
    ct = joblib.load("column_transformer.joblib")
    return model, ct


# Function to preprocess input data and predict rent
def predict_rent(
    model,
    ct,
    location,
    junction_dist,
    house_size,
    num_rooms,
    furnished,
    parking,
    water_electricity,
):
    # Create a DataFrame with the input values
    input_data = pd.DataFrame(
        {
            "Location": [location],
            "Distance from Junction": [junction_dist],
            "Size of House": [house_size],
            "Number of Rooms": [num_rooms],
            "Distance from Metro": [0],  # Set as 0 for prediction
            "Furnished": [furnished],
            "Parking": [parking],
            "Water & Electricity": [water_electricity],
        }
    )

    # Perform encoding for categorical variables
    input_data_encoded = ct.transform(input_data)

    # Use the trained model to predict the rent
    predicted_rent = model.predict(input_data_encoded)[0]
    return predicted_rent
