import streamlit as st
from langchain import LangChain
from langchain.community import GoogleGenAI  # Correcting the import path

lang_chain = LangChain(api_key="your_langchain_api_key")
google_genai_service = GoogleGenAI(api_key="your_google_genai_api_key")

def main():
    st.title("AI-Powered Travel Planner")

    source = st.text_input("Enter Source Location")
    destination = st.text_input("Enter Destination Location")

    if st.button("Find Travel Options"):
        if source and destination:
            travel_options = get_travel_options(source, destination)
            display_travel_options(travel_options)
        else:
            st.warning("Please enter both source and destination.")

def display_travel_options(travel_options):
    for option in travel_options:
        st.write(f"Mode: {option['mode']}, Cost: {option['cost']}")

def get_travel_options(source, destination):
    query = f"Find travel options from {source} to {destination}"
    langchain_response = lang_chain.ask(query)
    genai_response = google_genai_service.analyze(query=query)
    travel_options = combine_responses(langchain_response, genai_response)
    return travel_options

def combine_responses(langchain_response, genai_response):
    # Combine the responses from both LangChain and Google GenAI
    travel_options = []
    # Example combining logic
    travel_options.extend(parse_response(langchain_response))
    travel_options.extend(parse_response(genai_response))
    return travel_options

def parse_response(response):
    # Dummy parsing function, replace with actual parsing logic
    travel_options = [
        {"mode": "Cab", "cost": 50},
        {"mode": "Train", "cost": 30},
        {"mode": "Bus", "cost": 20},
        {"mode": "Flight", "cost": 100},
    ]
    return travel_options

if __name__ == "__main__":
    main()
