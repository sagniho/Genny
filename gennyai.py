import streamlit as st
import openai
from openai import OpenAI
import base64
import re

st.set_page_config(page_title="Genny AI Website Advisor", page_icon="gen.png")
# Set your OpenAI API key
# Access API key from environment variable
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

def remove_source_tag(text):
    # Use a regular expression to find and remove the source tag pattern
    pattern = r"&#8203;``【oaicite:2】``&#8203;"
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

# Use the Assistant ID from the Assistant you created
ASSISTANT_ID = st.secrets['GENNY_ASSISTANT_ID_v2']
with st.sidebar:
    st.image("bench.png", use_column_width="auto")
    st.subheader("Welcome to the [Benchmark Gensuite®.](https://benchmarkgensuite.com) Unified, organically developed, and integrated digital solutions for EHS, sustainability, quality, operational risk, product stewardship, supply chain, and ESG disclosure reporting.  ")

# Create columns for the logo and the title
col1, col2 = st.columns([1, 4])

# In the first column, display the logo
with col1:
    st.image('genny.png', width=175)  # Adjust the width as needed

# In the second column, display the title and subtitle
with col2:
    st.markdown("<h2 style='margin-top: 0;'>Benchmark Gensuite® Product Advisor</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin-top: 0; padding-left: 10px;'>Your interactive Genny AI-powered guide to the Benchmark Gensuite solutions platform</p>", unsafe_allow_html=True)


def send_message_get_response(assistant_id, user_message):
    # Create a new thread
    thread = client.beta.threads.create()

    # Add user message to the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Retrieve the assistant's response
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            return text


def main():
    # Initialize messages in session state if not present
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Show quick ask questions if none have been asked or typed yet
    if 'quick_asked' not in st.session_state:
        st.session_state['quick_asked'] = False

    if not st.session_state['quick_asked']:
        quick_questions = [
            "How do I get started?",
            "What should I implement?",
            "Why select Benchmark Gensuite?"
        ]
        # Use a single row for quick ask questions
        cols = st.columns(len(quick_questions))
        for col, question in zip(cols, quick_questions):
            if col.button(question):
                # Mark as asked and process the question
                st.session_state['quick_asked'] = True
                process_user_input(question)

    # User input for new message
    user_input = st.text_input("Please ask me your question…", key="user_input")

    # If a quick ask question has been selected or user has typed a question, process it
    if user_input and not st.session_state['quick_asked']:
        # Mark as asked and process the typed question
        st.session_state['quick_asked'] = True
        process_user_input(user_input)

    # Display previous chat messages
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            with st.chat_message("user", avatar="🧑‍💻"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar="genn.png"):
                st.write(msg["content"])

def process_user_input(input_text):
    # Append the message to the session state
    st.session_state['messages'].append({'role': 'user', 'content': input_text})
    # Display the user message
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(input_text)

    # Get the response from the assistant
    with st.spinner('Working on this for you now...'):
        response = send_message_get_response(ASSISTANT_ID, input_text)
        cleaned_response = remove_source_tag(response)
        # Append the response to the session state
        st.session_state['messages'].append({'role': 'assistant', 'content': cleaned_response})
        # Display the assistant's response
        with st.chat_message("assistant", avatar="genny.png"):
            st.write(cleaned_response)



if __name__ == "__main__":
    main()