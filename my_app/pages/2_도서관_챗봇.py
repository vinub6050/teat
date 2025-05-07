import streamlit as st
from openai import OpenAI

st.title("📚 국립부경대학교 도서관 챗봇")

library_rules = """
[여기에 국립부경대학교 도서관 규정 내용을 붙여 넣으세요]
"""

api_key = st.text_input("OpenAI API Key", type="password")
question = st.text_area("도서관 규정 관련 질문을 입력하세요.")

if api_key and question and st.button("질문하기"):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"너는 국립부경대학교 도서관 규정에 대해 답변하는 챗봇이야. 규정 내용:\n{library_rules}"},
            {"role": "user", "content": question}
        ]
    )
    st.write(response.choices[0].message.content.strip())
