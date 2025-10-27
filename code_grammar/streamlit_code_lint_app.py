import streamlit as st
import openai
import ast
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 불러오기
def get_api_key():
    return os.getenv("OPENAI_API_KEY")

def check_syntax(code):
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        return str(e)

def chatgpt_suggest_fixes(code, prompt="코드를 개선하고 오류를 수정해주세요."):
    api_key = get_api_key()
    if not api_key:
        return "환경 변수에 OPENAI_API_KEY가 설정되어 있지 않습니다."
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 숙련된 Python 코드 리뷰어입니다."},
                {"role": "user", "content": f"다음 파이썬 코드를 개선하고 오류를 수정해주세요.\n\n{code}"}
            ],
            temperature=0
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"오류 발생: {e}"

def main():
    # 페이지 레이아웃 및 스타일
    st.set_page_config(page_title="Python 코드 검사기", page_icon="🐍", layout="wide")

    st.markdown("""
        <style>
        .main {background-color: #f9fafb;}
        .stButton>button {
            background-color: #2563eb;
            color: white;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            font-size: 1em;
        }
        .stButton>button:hover {
            background-color: #1d4ed8;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🖥️ Python 코드 문법 검사 & ChatGPT 수정기")
    st.markdown("""
    이 앱은 **Python 코드 문법 오류를 검사**하고, 필요하다면 **ChatGPT가 자동으로 코드 개선 및 수정**을 제안해줍니다.
    """)

    col1, col2 = st.columns([2, 1])
    with col1:
        code = st.text_area("⌨️ 파이썬 코드 입력", height=300, placeholder="여기에 코드를 입력하세요...")
    with col2:
        st.markdown("""
        ### 사용 방법
        1. 코드 입력
        2. **문법 검사** 버튼 클릭 → 오류 여부 확인
        3. **ChatGPT로 코드 수정** 버튼 클릭 → 수정된 코드 제안
        """)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ 문법 검사"):
            error = check_syntax(code)
            if error:
                st.error(f"문법 오류: {error}")
            elif not code.strip():
                st.warning("코드를 입력해주세요.")
            else:
                st.success("문법 오류 없음!")
            

    with c2:
        if st.button("🤖 ChatGPT로 코드 수정"):
            if not code.strip():
                st.warning("코드를 입력해주세요.")
            else:
                with st.spinner("ChatGPT가 코드를 수정 중입니다..."):
                    fixed_code = chatgpt_suggest_fixes(code)
                    st.subheader("🛠️ 수정된 코드 제안")
                    st.code(fixed_code, language="python")

if __name__ == "__main__":
    main()