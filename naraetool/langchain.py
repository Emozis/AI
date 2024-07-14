import os 
from dotenv import load_dotenv 

def check_api_key(api_name:str) -> None:
    """환경변수에 API가 있는지 확인하는 함수

    Args:
        api_name (str): 확인할 API KEY의 key 값
    """
    load_dotenv()

    if api_name not in os.environ:
        print(f"{api_name} 정보가 없습니다. 확인 후 환경변수에 등록해주세요.")