import streamlit as st
from openai import OpenAI

# API Key를 session_state로 저장하여 페이지 이동 후에도 유지되도록
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

# API Key 입력받기
api_key_input = st.text_input("OpenAI API Key", type="password", value=st.session_state.api_key)

# API Key가 변경되었으면 session_state에 저장
if api_key_input != st.session_state.api_key:
    st.session_state.api_key = api_key_input

# OpenAI 클라이언트 생성
if st.session_state.api_key:
    client = OpenAI(api_key=st.session_state.api_key)

# Streamlit 앱 제목
st.title("OpenAI GPT model")

# 사용자 입력 받기
prompt = st.text_area("User prompt")

# 'Ask!' 버튼 클릭 시 응답 받기
if st.button("Ask!", disabled=(len(prompt) == 0)):
    if st.session_state.api_key:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        st.write(response.output_text)
    else:
        st.error("Please enter a valid API Key.")
