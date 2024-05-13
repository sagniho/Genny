import streamlit as st
import openai
from openai import OpenAI
import base64
import streamlit as st
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["Impact"]

st.set_page_config(page_title="Impact 2024 Genny AI", page_icon="gen.png")

with st.sidebar:
    st.image("bench.png", use_column_width="auto")
    st.subheader("Welcome to [Benchmark Gensuite®.](https://benchmarkgensuite.com) Unified, organically developed, and integrated digital solutions for EHS, sustainability, quality, operational risk, product stewardship, supply chain, and ESG disclosure reporting.")

# Create columns for the logo and the title
col1, col2 = st.columns([1, 4])

with col1:
    st.image('genny.png', width=175)

with col2:
    st.markdown("<h2 style='margin-top: 0;'>Impact 2024 Genny AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin-top: 0; padding-left: 5px; color: green; font-style: italic;'>Your interactive Genny AI-powered guide to Impact 2024</p>", unsafe_allow_html=True)

def send_message_get_response(assistant_id, user_message, thread_id):
    if 'thread_id' not in st.session_state or st.session_state['thread_id'] is None:
        thread = client.beta.threads.create()
        st.session_state['thread_id'] = thread.id
        thread_id = thread.id
    else:
        thread_id = st.session_state['thread_id']

    client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_message)
    run = client.beta.threads.runs.create(
        thread_id=thread_id, 
        assistant_id=assistant_id,
        additional_instructions="The user talking to you right now is Mukund, the CEO of Benchmark Gensuite, giving his opening keynote presentation on Day 2 (May 15). Have an interactive conversation with him, sort of like you're co-presenting the keynote. Have a back and forth with Mukund (ie, pass it back to him), while remembering that there is an audience in front of you both to whom you are both presenting. Tasteful puns, simple language without over-embellishing adjectives.",
        #additional_instructions="This user talking to you is: Bruno Nutti, Whirlpool, Global EHS Sr Analyst.  Bruno's next two sessions from now are:  Thursday May 16, 8:30 AM – 10:00 AM, Incident Management & Occupational Health, Location: Meeting Room 2-3; Thursday May 16, 10:30 AM – 12:00 PM,  Ergonomics, Location: Meeting Room 4-5. Bruno's conference point score is 85 and he is 5 on the leaderboard.",
        tool_choice="required"
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run.status == "completed":
            break

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    latest_message = messages.data[0]  # assuming the latest message is the response
    text = latest_message.content[0].text.value

    return text, thread_id

def main():
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    if 'thread_id' not in st.session_state:
        st.session_state['thread_id'] = None

    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            with st.chat_message("user", avatar="🧑‍💻"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar="genn.png"):
                st.write(msg["content"])

    user_input = st.chat_input(placeholder="Please ask me your question…")
    if user_input:
        process_user_input(user_input)

def process_user_input(user_input):
    st.session_state['messages'].append({'role': 'user', 'content': user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(user_input)

    with st.spinner('Working on this for you now...'):
        response, thread_id = send_message_get_response(ASSISTANT_ID, user_input, st.session_state['thread_id'])
        st.session_state['thread_id'] = thread_id
        st.session_state['messages'].append({'role': 'assistant', 'content': response})
        with st.chat_message("assistant", avatar="genn.png"):
            st.write(response)

if __name__ == "__main__":
    main()
