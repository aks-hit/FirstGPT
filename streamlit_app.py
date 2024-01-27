# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

from openai import OpenAI
import streamlit as st


# Ask the user's api key
with st.form('form'):
    user_api_key = st.text_input('Enter OpenAI API token:', type='password')
    submit = st.form_submit_button('Submit')

if submit:
    if len(user_api_key) == 51 and user_api_key.startswith('sk-'):
        client = OpenAI(api_key=user_api_key)
        st.success('api key is successfully entered')
    else:
        st.error('Your api key is invalid.')
        st.stop()

# Make the client visible to other codes below it. 
client = OpenAI(api_key=user_api_key)

# Your other stuff
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]}
                  for m in st.session_state.messages], stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
