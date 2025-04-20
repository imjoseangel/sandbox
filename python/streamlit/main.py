import streamlit as st
import pandas as pd

# Load the Iris dataset
df = pd.read_csv('iris.csv')

# Set the title of the app
st.title("Iris Dataset Explorer")

# Display the entire dataframe
st.write("### Full Iris Dataset")
st.dataframe(df)

# Sidebar configuration
st.sidebar.header("Filter Options")

# Feature selection
feature = st.sidebar.selectbox(
    "Select a feature to filter by:", df.columns[:-1])

# Range selection based on the selected feature
min_value = float(df[feature].min())
max_value = float(df[feature].max())

range_slider = st.sidebar.slider(
    f"Select range of {feature}:", min_value, max_value, (min_value, max_value))

# Filter the dataframe based on the selected range
filtered_df = df[(df[feature] >= range_slider[0]) &
                 (df[feature] <= range_slider[1])]

# Display the filtered dataset
st.write(
    f"### Filtered Iris Dataset by {feature} between {range_slider[0]} and {range_slider[1]}")
st.dataframe(filtered_df)

# Display basic statistics for the filtered data
st.write(f"### Statistics for {feature}")
st.write(filtered_df[feature].describe())
