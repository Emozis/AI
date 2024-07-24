import os
import streamlit as st
from pathlib import Path 
from .langchain import check_api_key
import base64

def setting():
    os.environ["LANGCHAIN_PROJECT"] = "GEMINI_PROJECT"
    check_api_key("GOOGLE_API_KEY")
    read_mdfile("./docs/css.md")


def read_mdfile(filepath:str) -> str:
    """markdown 파일을 읽고 텍스트로 반환하는 함수

    Args:
        filepath (str): markdown 파일 경로

    Returns:
        str: markdown 파일에서 추출된 텍스트
    """
    file = Path(filepath)
    
    if not file.is_file():
        file_text = f"[ERROR] 파일 경로를 찾을 수 없습니다.(INPUT PATH: {filepath})"
    else:
        file_text = file.read_text(encoding="utf-8")

    return st.markdown(file_text, unsafe_allow_html=True)

