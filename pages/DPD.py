from dotenv import load_dotenv
load_dotenv()  # loading all the environment variables

import streamlit as st
import os
import pandas as pd
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# Configure Gemini Pro model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Function to get response from Gemini Pro
def get_gemini_response(question):
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return ' '.join([chunk.text for chunk in response])

# Initialize Streamlit app
st.set_page_config(page_title="Draup Bot")
st.header("Gemini for Draup")

# File uploader
uploaded_file = st.file_uploader("Upload CSV file with prompts", type=["csv"])

# Rate-limiting variables
MAX_QUERIES_PER_MINUTE = 50
queries_this_minute = 0
minute_window_start = datetime.now()

if uploaded_file:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Check if 'response' column exists, if not, create it
    if 'response' not in df.columns:
        df['response'] = ''

    # Initialize progress bar
    progress_bar = st.progress(0)

    # Button to start processing
    if st.button("Start Processing"):
        for index, row in df.iterrows():
            # Check rate limit
            current_time = datetime.now()
            if current_time - minute_window_start >= timedelta(minutes=1):
                minute_window_start = current_time
                queries_this_minute = 0

            if queries_this_minute >= MAX_QUERIES_PER_MINUTE:
                # Wait until the next minute
                time_to_wait = 2 - (current_time - minute_window_start).seconds
                time.sleep(time_to_wait)
                minute_window_start = datetime.now()
                queries_this_minute = 0

            if pd.isna(row['response']) or row['response'] == '':
                response = get_gemini_response(row['prompt'])
                df.at[index, 'response'] = response
                queries_this_minute += 1

            progress_percentage = int((index + 1) / len(df) * 100)
            progress_bar.progress(progress_percentage)
            time.sleep(1)  # Small delay for UI update

        st.success("Processing complete.")

    # Show the DataFrame in Streamlit
    st.markdown("## Responses")
    st.dataframe(df)

    # Save the updated DataFrame as a CSV file and allow user to download it
    if len(df) > 0 and all(df['response'] != ''):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download updated CSV",
            data=csv,
            file_name='ETL_Extract.csv',
            mime='text/csv',
        )
