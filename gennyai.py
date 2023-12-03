import streamlit as st
import openai
from openai import OpenAI
import base64
# Set your OpenAI API key
# Access API key from environment variable
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]



client = OpenAI(api_key=OPENAI_API_KEY)

# Use the Assistant ID from the Assistant you created
ASSISTANT_ID = st.secrets['GENNY_ASSISTANT_ID']
with st.sidebar:
    st.image("bench.png", use_column_width="auto")
    "[Benchmark Gensuite](https://benchmarkgensuite.com)"
    st.subheader("Welcome to Genny AI - Benchmark Gensuite's customer AI assistant", anchor=None,help=None, divider="blue")
   

st.title("GennyAI")
st.caption("Your Benchmark Gensuite Advisor")

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


    # Display previous chat messages
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            with st.chat_message("user", avatar="🧑‍💻"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar="genny.png"):
                st.write(msg["content"])
    # Chat input for new message
    user_input = st.chat_input()

    # When a message is sent through the chat input
    if user_input:
        # Append the user message to the session state
        st.session_state['messages'].append({'role': 'user', 'content': user_input})

        # Get the response from the assistant
        with st.spinner('Thinking...'):
            response = send_message_get_response(ASSISTANT_ID, user_input)

        # Append the response to the session state
        st.session_state['messages'].append({'role': 'assistant', 'content': response})

        # Update the page to display the new messages
        st.experimental_rerun()

if __name__ == "__main__":
    main()