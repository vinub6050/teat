import streamlit as st
from openai import OpenAI

# 초기 세션 상태 설정
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# API 키 입력 받기 (세션에 저장)
api_key_input = st.text_input("🔐 OpenAI API Key", type="password", value=st.session_state.api_key)
if api_key_input != st.session_state.api_key:
    st.session_state.api_key = api_key_input

# 클라이언트 생성
if st.session_state.api_key:
    client = OpenAI(api_key=st.session_state.api_key)

st.title("💬 OpenAI GPT Chat")

# 사용자 프롬프트 입력
prompt = st.text_area("👤 User Prompt", height=100)

# 버튼 UI
col1, col2 = st.columns([1, 1])
ask = col1.button("🚀 Ask", disabled=(len(prompt.strip()) == 0))
clear = col2.button("🧹 Clear")

# Ask 버튼 눌렀을 때
if ask and st.session_state.api_key:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # gpt-4.1-mini 는 현재 지원 안됨
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()

        # 대화 저장
        st.session_state.chat_history.append(("You", prompt))
        st.session_state.chat_history.append(("GPT", answer))

    except Exception as e:
        st.error(f"❌ API 요청 실패: {e}")

# Clear 버튼 눌렀을 때
if clear:
    st.session_state.chat_history = []

# 대화 출력
if st.session_state.chat_history:
    st.markdown("### 🧾 대화 기록")
    for role, message in st.session_state.chat_history:
        st.markdown(f"**{role}:** {message}")

elif not st.session_state.api_key:
    st.warning("먼저 유효한 OpenAI API 키를 입력해주세요.")
