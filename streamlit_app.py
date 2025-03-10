import streamlit as st
import numpy as np
import pandas as pd
import requests

# Function to map cluster predictions to meaningful labels
# (Not used if the API already returns the label as a string)
def rename_clusters(cluster_id):
    cluster_mapping = {
        1: "Running",
        0: "Concluded",
        2: "Blockbuster"
    }
    return cluster_mapping.get(cluster_id, "Unknown")

# Original Background Video CSS (Unchanged)
def set_css():
    st.markdown("""
        <style>
            #myVideo {
                position: fixed;
                right: 0;
                bottom: 0;
                min-width: 100%; 
                min-height: 100%;
            }
            .content {
                position: fixed;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                color: #f1f1f1;
                width: 100%;
                padding: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

# Embed Background Video (Unchanged)
def embed_video():
    video_link = "https://res.cloudinary.com/dipr3sq8j/video/upload/v1741559411/Untitled-design_xii7rf.mp4"
    st.markdown(f"""
        <video autoplay muted loop id="myVideo">
            <source src="{video_link}">
            Your browser does not support HTML5 video.
        </video>
    """, unsafe_allow_html=True)

# Function to predict using the API (Integration of API instead of local model)
def predict_via_api(data):
    url = 'https://project-8-ndx5.onrender.com/predict'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    formatted_data = {
        "run_length": data['run_length'],
        "ongoing": "Yes" if data['ongoing'] == 1 else "No",
        "imdb_rating": data['IMDb Rating'],
        "total_ratings": data['Total Ratings']
    }
    try:
        response = requests.post(url, headers=headers, json=formatted_data)
        if response.status_code == 200:
            print(response.json())  # For debugging
            return response.json().get('predicted_category')
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error: {e}"

# Main App Content – Clustering Model Integration via API
def main_content():
    st.title(":clapper: :red[Show Category Prediction App]")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Enter Show Details")
        imdb_rating = st.number_input("IMDb Rating", min_value=0.0, max_value=10.0, step=0.1)
        total_ratings = st.number_input("Total Ratings", min_value=0, step=100)
        run_length = st.number_input("Run Length (in years)", min_value=1, step=1)
        ongoing = st.selectbox("Is the show ongoing?", ["Yes", "No"])

        # Map user inputs to numerical values
        test_data = {
            'IMDb Rating': imdb_rating,
            'Total Ratings': total_ratings,
            'run_length': run_length,
            'ongoing': 1 if ongoing == "Yes" else 0,
        }

        if st.button("Predict Category"):
            prediction = predict_via_api(test_data)
            # Use the API's prediction directly since it's already a string label
            predicted_label = prediction
            st.success(f"**The predicted category is:** {predicted_label}")

    with col2:
        st.subheader("Model Comparison")
        st.markdown("**Silhouette Scores:**")
        st.markdown("- **K-Means:** `0.5278` (Higher Score)")
        st.markdown("- **DBSCAN:** `0.5063`")
        st.markdown("> **K-Means** performed slightly better based on the Silhouette Score, indicating better-defined clusters.")

if __name__ == "__main__":
    set_css()
    embed_video()
    main_content()
