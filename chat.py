import openai
import streamlit as st

st.title("ChatGPT-like clone")

ANYSCALE_API = st.secrets["anyscale_apikey"]

openai.api_key = ANYSCALE_API
openai.api_base = "https://api.endpoints.anyscale.com/v1"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "mistralai/Mistral-7B-Instruct-v0.1"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Maximum allowed messages
max_messages = (
    20  # Counting both user and assistant messages, so 10 iterations of conversation
)

if len(st.session_state.messages) >= max_messages:
    st.info(
        """Notice: The maximum message limit for this demo version has been reached. We value your interest!
        We encourage you to experience further interactions by building your own application with instructions
        from Streamlit's [Build conversational apps](https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps)
        tutorial. Thank you for your understanding."""
    )

else:
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
