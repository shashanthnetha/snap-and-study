import streamlit as st
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE


st.set_page_config(
    page_title="Snap & Study",
    layout="centered"
)


api_key = st.secrets["GEMINI_API_KEY"]
model = "gemini-3.1-flash-lite"


@st.cache_resource
def get_client():
    return genai.Client(api_key=api_key)


client = get_client()


if "messages" not in st.session_state:
    st.session_state.messages = []

    st.session_state.messages.append({
        "role": "assistant",
        "content": WELCOME_MESSAGE
    })


st.title("Snap & Study")
st.caption("A simple study buddy to help you understand difficult topics.")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("image"):
            st.image(message["image"])

        if message.get("content"):
            st.write(message["content"])


user_input = st.chat_input(
    "Ask a question or attach an image",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"]
)


if user_input:
    question = user_input.text
    image = user_input.files[0] if user_input.files else None

    if image:
        image_bytes = image.getvalue()

        st.session_state.messages.append({
            "role": "user",
            "content": question,
            "image": image_bytes
        })

        with st.chat_message("user"):
            st.image(image_bytes)

            if question:
                st.write(question)

        parts = [
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=image.type
            )
        ]

        if question:
            parts.append(question)
        else:
            parts.append(
                "Explain what is shown in this image in simple language."
            )

    else:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.write(question)

        parts = [question]

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                conversation = []

                for message in st.session_state.messages[:-1]:
                    if message.get("content"):
                        conversation.append(
                            f"{message['role']}: {message['content']}"
                        )

                previous_messages = "\n".join(conversation)

                prompt = SYSTEM_PROMPT

                if previous_messages:
                    prompt += (
                        "\n\nPrevious conversation:\n"
                        + previous_messages
                    )

                parts.insert(0, prompt)

                response = client.models.generate_content(
                    model=model,
                    contents=parts
                )

                answer = response.text

            except Exception as e:
                answer = f"Something went wrong: {e}"

        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
