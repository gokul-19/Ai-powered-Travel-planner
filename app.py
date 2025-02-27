import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.retry import Retry

# Set environment variable for DNS resolver
os.environ["GRPC_DNS_RESOLVER"] = "native"

# Initialize the Streamlit app
st.set_page_config(page_title="AI Yatra Guide", layout="wide")
st.title("🇮🇳 AI Yatra Guide 🚆")

# Retrieve API Key from Streamlit Secrets
api_key = st.secrets["api"].get("GOOGLE_GEMINI_API_KEY", None)

# Initialize LLM if API key is available
llm = None
if api_key:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key,
            temperature=0.7,
            retry=Retry(initial=1.0, maximum=60.0, multiplier=2.0, deadline=900.0)
        )
    except Exception as e:
        st.error(f"Invalid API Key or authentication error: {e}")

# User input
source = st.text_input("Source Location:")
destination = st.text_input("Destination Location:")
travel_mode = st.selectbox("Travel Mode:", ["All", "Train", "Bus", "Flight"], index=0)
travel_preference = st.selectbox("Travel Preference:", ["Budget", "Fastest", "Most Comfortable"], index=0)
sort_by = st.selectbox("Sort Results By:", ["Price", "Duration", "Departure Time"], index=0)
language = st.selectbox("Language:", ["English", "Hindi", "Tamil", "Telugu", "Kannada", "Marathi"], index=0)

# Generate travel recommendations
if st.button("Search Travel Options") and llm:
    if source and destination:
        prompt = f"""
        Provide travel options from {source} to {destination} using {travel_mode}.
        Prioritize {travel_preference} travel options.
        Sort results by {sort_by}.
        Respond in {language}.
        Include estimated costs and duration in bullet points.
        """

        try:
            response = llm.invoke([{"role": "user", "content": prompt}])
            st.success("✈️ Travel Recommendations:")
            st.write(response.content)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter both source and destination locations.")
