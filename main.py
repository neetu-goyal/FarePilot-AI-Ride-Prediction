# =====================================
# OUTLIER DETECTION SYSTEM
# =====================================

import pandas as pd
import streamlit as st
import numpy as np
import joblib

# Load Dataset
df = pd.read_csv("uber.csv")

# Select Completed Rides
completed_df = df[
    df["status"].str.lower() == "completed"
].copy()


# Function to calculate IQR limits
def calculate_iqr_limits(data, column):

    Q1 = data[column].quantile(0.25)

    Q3 = data[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR

    upper_limit = Q3 + 1.5 * IQR

    return lower_limit, upper_limit


# Calculate Fare Outlier Limits
fare_lower, fare_upper = calculate_iqr_limits(
    completed_df, "fare_amount"
)

# Calculate Distance Outlier Limits
distance_lower, distance_upper = calculate_iqr_limits(
    completed_df, "distance_km"
)

import pandas as pd
import streamlit as st

df = pd.read_csv("uber.csv")

st.title("Uber Fare Prediction")

st.success("Dataset Loaded Successfully!")

# First 5 rows
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Total rows and columns
st.subheader("Dataset Shape")
st.write(df.shape)

# Column names
st.subheader("Dataset Columns")
st.write(df.columns.tolist())

