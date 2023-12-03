import streamlit as st
import openai
from openai import OpenAI
from config import OPENAI_API_KEY  # Import the API key from config.py
from config import GENNY_ASSISTANT_ID
# Set your OpenAI API key
openai.api_key = 'OPENAI_API_KEY'
client = OpenAI(api_key="OPENAI_API_KEY")

# Use the Assistant ID from the Assistant you created
ASSISTANT_ID = 'GENNY_ASSISTANT_ID'


def send_message_get_response(assistant_id, thread_id, user_message):
    # Add user message to the thread
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=user_message
    )

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # Retrieve the assistant's response
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            return text


from streamlit_chat import message as st_message  # You may need to install streamlit-chat for this

# Assuming 'client' has been initialized as shown in the provided sample code


def main():
    st.markdown("""
        <style>
            .centered {
                text-align: center;
            }
            .stTextInput {
                width: 100%;
                margin: 10px 0;
            }
            .stButton > button {
                width: 100%;
                padding: 15px 30px;
                margin: 10px 0;
                border-radius: 25px;
                font-weight: bold;
            }
            .chatbox-padding {
                padding: 10px;
            }
            img {
                max-width: 100%;
                height: auto;
            }
        </style>
    """, unsafe_allow_html=True)

    # Create history and thread_id if not in the session state
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'thread_id' not in st.session_state:
        thread = client.beta.threads.create()
        st.session_state['thread_id'] = thread.id

    image = 'genny.png'
    st.image(image, width=50,)
    st.markdown("<h1 class='centered'>Genny AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='centered'>Your Benchmark Gensuite advisor</h3>", unsafe_allow_html=True)
    st.markdown("<p class='centered'><a href='https://www.benchmarkgensuite.com' target='_blank'>www.benchmarkgensuite.com</a></p>", unsafe_allow_html=True)


   

    # Chat history display
    for idx, message in enumerate(st.session_state['history'][::-1]):
        st.text_area(label='', value=message['text'], key=f"msg_{idx}", height=75, disabled=True)

    with st.form(key='my_form', clear_on_submit=True):
	    user_input = st.text_input('What would you like to ask Genny', key='user_input')
	    submit_button = st.form_submit_button('Send')
	    if submit_button:
	        if user_input:
	            st.session_state['history'].append({'text': user_input, 'is_user': True})
	            response = send_message_get_response(ASSISTANT_ID, st.session_state['thread_id'], user_input)
	            st.session_state['history'].append({'text': response, 'is_user': False})
	            st.experimental_rerun()
	        else:
	            st.warning("Please enter a message.")

if __name__ == "__main__":
    main()
