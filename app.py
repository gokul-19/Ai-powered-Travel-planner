import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.retry import Retry

# Set environment variable for DNS resolver
os.environ["GRPC_DNS_RESOLVER"] = "native"

# Initialize the Streamlit app
st.set_page_config(page_title="AI Travel Planner", layout="wide")
st.title("AI-Powered Travel Planner")

# Retrieve API Key from Streamlit Secrets
st.session_state.api_key = st.secrets["api"].get("GOOGLE_GEMINI_API_KEY", None)

# Initialize LLM if API key is available
if st.session_state.api_key:
    try:
        st.session_state.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=st.session_state.api_key,
            temperature=0.7,
            retry=Retry(initial=1.0, maximum=60.0, multiplier=2.0, deadline=900.0)
        )
    except Exception as e:
        st.error(f"Invalid API Key or authentication error: {e}")
        st.session_state.llm = None
else:
    st.session_state.llm = None
    st.error("API Key not found. Please configure it in Streamlit Secrets.")

# User input
source = st.text_input("Source Location:", "")
destination = st.text_input("Destination Location:", "")
travel_mode = st.selectbox("Travel Mode:", ["All", "Train", "Bus", "Flight"], index=0)

# Generate travel recommendations
if st.button("Search Travel Options") and st.session_state.llm:
    if not source or not destination:
        st.warning("Please enter both source and destination locations")
    else:
        prompt = f"Provide travel options from {source} to {destination} using {travel_mode}. " \
                 "Include estimated costs and duration. Format as bullet points."

        try:
            response = st.session_state.llm.invoke([{"role": "user", "content": prompt}])
            st.success("✈️ Travel Recommendations:")
            st.write(response.content)
        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    st.warning("Please ensure an API Key is configured in Streamlit Secrets.")
