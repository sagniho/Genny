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
    st.subheader("Welcome to the [Benchmark Gensuite®](https://benchmarkgensuite.com) Genny AI Website Assistant")
st.markdown("""
    <div style="display: flex; align-items: center;">
        <img src="genny.png" style="width: 50px; height: 50px; margin-right: 10px;">
        <div>
            <h1 style="margin: 0;">Genny AI Website Assistant</h1>
            <p style="margin: 0;">Your Benchmark Gensuite® Solutions Advisor</p>
        </div>
    </div>
""", unsafe_allow_html=True)

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
            st.chat_message(msg["content"], avatar="🧑‍💻", is_user=True)
        else:
            st.chat_message(msg["content"], avatar="genny.png", is_user=False)

    # Chat input for new message
    user_input = st.chat_input(placeholder="Please ask me your question…")

    # When a message is sent through the chat input
    if user_input:
        # Append the user message to the session state
        st.session_state['messages'].append({'role': 'user', 'content': user_input})
        # Display the user message
        st.chat_message(user_input, avatar="🧑‍💻", is_user=True)

        # Get the response from the assistant
        with st.spinner('Working on this for you now...'):
            response = send_message_get_response(ASSISTANT_ID, user_input)
            # Append the response to the session state
            st.session_state['messages'].append({'role': 'assistant', 'content': response})
            # Display the assistant's response
            st.chat_message(response, avatar="genny.png", is_user=False)



if __name__ == "__main__":
    main()