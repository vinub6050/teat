import streamlit as st
from openai import OpenAI
import tempfile
import os
import PyPDF2

st.title("📄 ChatPDF - PDF 기반 챗봇")

# API 키 입력
api_key = st.text_input("OpenAI API Key", type="password")
if not api_key:
    st.warning("OpenAI API Key를 입력하세요.")
    st.stop()

client = OpenAI(api_key=api_key)

# 파일 업로드
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf", accept_multiple_files=False)

# 상태 초기화
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "vector_cleared" not in st.session_state:
    st.session_state.vector_cleared = False

# Clear 버튼 처리
if st.button("Clear"):
    st.session_state.pdf_text = ""
    st.session_state.vector_cleared = True
    st.success("Vector store가 초기화되었습니다.")

# PDF 업로드 후 텍스트 추출
if uploaded_file and not st.session_state.vector_cleared:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with open(tmp_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        st.session_state.pdf_text = text

    os.remove(tmp_path)

# 사용자 질문 입력
user_input = st.text_area("PDF 내용을 기반으로 질문하세요:")

if st.button("질문하기") and user_input and st.session_state.pdf_text:
    messages = [
        {"role": "system", "content": "다음은 사용자가 업로드한 PDF 문서의 내용입니다. 이 내용을 바탕으로 질문에 답하세요."},
        {"role": "system", "content": st.session_state.pdf_text[:3000]},  # OpenAI context 제한을 고려해 일부만
        {"role": "user", "content": user_input}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    st.write(response.choices[0].message.content.strip())