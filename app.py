import streamlit as st
from langchain.llms import GoogleGenAI
import requests

# Initialize Google GenAI model (replace 'your-api-key' with actual API key)
llm = GoogleGenAI(api_key="your-api-key")

def fetch_travel_data(source, destination):
    """Fetch real-time travel data from APIs (placeholder function)."""
    # Example API calls (Replace with actual APIs like Google Maps, Skyscanner, IRCTC, etc.)
    travel_options = {
        "Cab": {"price": "₹1200", "duration": "2 hours"},
        "Train": {"price": "₹500", "duration": "3.5 hours"},
        "Bus": {"price": "₹400", "duration": "4 hours"},
        "Flight": {"price": "₹3500", "duration": "1 hour"},
    }
    return travel_options

# Streamlit UI
st.title("AI-Powered Travel Planner")
source = st.text_input("Enter Source Location:")
destination = st.text_input("Enter Destination Location:")

if st.button("Find Travel Options"):
    if source and destination:
        travel_data = fetch_travel_data(source, destination)
        prompt = f"Find the best travel option from {source} to {destination} given the choices: {travel_data}."
        response = llm.predict(prompt)
        
        st.subheader("Recommended Travel Option:")
        st.write(response)
        
        st.subheader("All Travel Options:")
        for mode, details in travel_data.items():
            st.write(f"**{mode}** - Price: {details['price']}, Duration: {details['duration']}")
    else:
        st.error("Please enter both source and destination.")
