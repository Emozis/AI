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

def pdf_viewer(filepath:str) -> None:
    """PDF 뷰어

    Args:
        filepath (str): pdf 파일 경로
    """
    file = Path(filepath)
    
    if not file.is_file():
        file_text = f"[ERROR] 파일 경로를 찾을 수 없습니다.(INPUT PATH: {filepath})"
        st.markdown(file_text)
    else:
        # pdf를 바이너리로 읽기
        with open(filepath, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        # Html로 임베딩하기
        pdf_display =  f"""
                        <embed
                        class="pdfobject"
                        type="application/pdf"
                        title="Embedded PDF"
                        src="data:application/pdf;base64,{base64_pdf}"
                        style="overflow: auto; width: 100%; height: 100%;">
                        """

        # 출력
        st.markdown(pdf_display, unsafe_allow_html=True)