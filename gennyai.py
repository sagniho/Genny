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
def send_quick_question(question):
    # Simulate sending a quick question
    st.session_state['user_input'] = question  # Prepopulate the input field
    st.session_state['messages'].append({'role': 'user', 'content': question})
    # Get the response from the assistant
    response = send_message_get_response(ASSISTANT_ID, question)
    # Append the response to the session state
    st.session_state['messages'].append({'role': 'assistant', 'content': response})

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

    # Define some quick questions for users to ask
    quick_questions = [
        "How do I get started?",
        "What should I implement?",
        "Why select Benchmark Gensuite?"
    ]

    # Display quick ask questions as buttons
    for question in quick_questions:
        if st.button(question):
            send_quick_question(question)
    # Initialize messages in session state if not present
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Display previous chat messages
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            with st.chat_message("user", avatar="🧑‍💻"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar="genn.png"):
                st.write(msg["content"])

    # Chat input for new message
    user_input = st.session_state.get('user_input', '')
    user_input_field = st.chat_input(placeholder="Please ask me your question…", key='user_input')

    # When a message is sent through the chat input
    if user_input_field:
        # Append the user message to the session state and display it
        st.session_state['messages'].append({'role': 'user', 'content': user_input_field})

        # Get the response from the assistant
        with st.spinner('Working on this for you now...'):
            response = send_message_get_response(ASSISTANT_ID, user_input_field)
            # Append the response to the session state
            st.session_state['messages'].append({'role': 'assistant', 'content': response})
    
    # Display messages
    for msg in st.session_state.messages:
        role = "user" if msg['role'] == 'user' else "assistant"
        avatar = "🧑‍💻" if role == "user" else "genn.png"
        with st.chat_message(role, avatar=avatar):
            st.write(msg['content'])

if __name__ == "__main__":
    main()