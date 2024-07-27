import os
from pathlib import Path 
import base64


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

