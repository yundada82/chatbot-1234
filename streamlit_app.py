import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("너를 위한 마음의 소리 Chatbot")
st.write("마음을 털어놓고 싶은 날, 위로와 응원이 필요한 순간, 당신을 위한 내가 여기 있습니다.\n\n"
         "처음 이용하시려면, 잠깐만 OpenAI API 키를 입력해 주세요. 🔑\n"
    "당신만의 대화를 만들기 위한 작은 열쇠예요. [API 키 받기](https://platform.openai.com/account/api-keys)"
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("🔑 대화를 시작하기 위한 나만의 열쇠 (OpenAI API Key)", type="password")
if not openai_api_key:
    st.info("조용히 당신의 이야기를 들어드릴 준비가 되어 있어요.\n위에 API 키만 입력해 주세요 ☕", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "너는 사람들의 고민이나 속마음을 공감하며 들어주는 따뜻한 대화 상대야. 절대 판단하지 않고, 부드럽고 진심 어린 말투로 이야기해줘."}]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("오늘 마음에 담아두었던 이야기가 있다면, 살며시 말해 주세요 💭"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o",
            temperature=1.2,
            max_tokens=300,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
    st.markdown("_잠시만요... 당신의 마음을 듣고 있어요 🤍_")  # 👈 여기 추가
    response = st.write_stream(stream)  # 응답 스트리밍
        st.session_state.messages.append({"role": "assistant", "content": response})
