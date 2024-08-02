import os
import streamlit as st
from pathlib import Path 
from dotenv import load_dotenv 
import base64

def setting(layout="centered"):
    st.set_page_config(layout=layout)
    load_dotenv()
    # check_api_key("GOOGLE_API_KEY")
    read_mdfile("./static/css/css.md")


def read_mdfile(filepath:str) -> st.markdown:
    """markdown 파일을 읽고 markdown으로 작성하는 함수

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


def read_prompt(filepath:str) -> str:
    """프롬프트 파일을 읽고 텍스트로 반환하는 함수

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

    return file_text


def vertical_space(size:int):
    """Create vertical blank spaces

    Args:
        size (int): height
    """
    st.container(height=size, border=False)

def input_text_align(text:str, font=16, align="center"):
    """Aligns the text with the specified alignment
    
    Args:
        text (str): The text to be aligned
        type (str, optional): The alignment style for the text. Can be one of the following: 'left', 'center'(default), 'right' 
    """
    st.markdown(f"""
               <div style="text-align:{align}; font-size:{font}px;">
               {text}
               </div>
               """, unsafe_allow_html=True)