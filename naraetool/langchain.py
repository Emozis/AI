import os 
import asyncio
import requests
import json
import streamlit as st
import time
from pathlib import Path 
from naraetool.main_logger import logger
from naraetool.main_config import configs
from google.api_core import exceptions

config = configs.model_info

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage,HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory

# 사용 안함
# def check_api_key(api_name:str) -> None:
#     """환경변수에 API가 있는지 확인하는 함수

#     Args:
#         api_name (str): 확인할 API KEY의 key 값
#     """
#     load_dotenv()

#     if api_name not in os.environ:
#         print(f"{api_name} 정보가 없습니다. 확인 후 환경변수에 등록해주세요.")

def validate_google_api_key():
    """Google API Key 유효성 검사하는 함수"""
    key_name = "GOOGLE_API_KEY"
    if key_name not in os.environ:
        return f"{key_name} 정보가 없습니다. 환경변수를 확인해주세요."
    
    result = requests.post(
        url= "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent",
        data=b'{"contents":[{"parts":[{"text":""}]}]}',
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": os.getenv(key_name)
        }
    )

    if result.status_code != 200:
        logger.debug(json.loads(result.content))
    
    logger.info("Google API Key validation succeeded.")

class Gemini:
    def __init__(self, input_vars, template_name):
        self.input_vars = input_vars
        self._transform()
        
        self.template_name = template_name
        self.model_name = config["model_name"]
        self.temperature = config["temperature"]

        self.chain = self._create_chain()

    @staticmethod
    def wrap_messages(chat_history):
        """chat_history에 Message 객체 씌우는 메서드"""
        if not chat_history:
            return []

        chat_messages = []
        for log in chat_history:
            if log["role"] == "user":
                chat = HumanMessage(log["content"])
            elif log["role"] == "character":
                chat = AIMessage(log["content"])
            
            chat_messages.append(chat)
        
        return chat_messages

    def _transform(self):
        """input_vars 를 변환하는 메서드"""
        # history Message 객체 씌우기
        history = self.input_vars["chat_history"]
        self.input_vars["chat_history"] = self.wrap_messages(history)

    @staticmethod
    def read_template(filename:str) -> str:
        """프롬프트 파일을 읽고 텍스트로 반환하는 함수

        Args:
            filepath (str): markdown 파일 경로

        Returns:
            str: markdown 파일에서 추출된 텍스트
        """
        file_path = Path(__file__).parents[1] / f"data/templates/{filename}"
        
        try:
            file_text = file_path.read_text(encoding="utf-8")
        except:
            file_text = ""
            logger.error(f"파일 경로를 찾을 수 없습니다.(INPUT PATH: {str(file_path)})")

        return file_text
    
    def _check_inputs_equal(self, prompt):
        """프롬프트와의 변수가 매칭되는지 체크하는 메서드"""
        input_vars = set(self.input_vars)
        prompt_vars = set(prompt.input_variables)
        if input_vars != prompt_vars:
            logger.error(f"input_vars does not match a variable in the prompt\n(input_vars):{input_vars} (prompt_vars):{prompt_vars}")

    def _get_prompts(self):
        """프롬프트 객체 만드는 메서드"""
        # 프롬프트 설정
        template = self.read_template(self.template_name)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", template),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        self._check_inputs_equal(prompt)

        return prompt

    def _create_chain(self):
        """Chain 만드는 메서드"""
        # 프롬프트 설정
        prompt = self._get_prompts()

        # 모델 설정
        model = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature
        )

        # 출력 파서 설정
        output_parser = StrOutputParser()

        # 체인 만들기
        chain = prompt | model | output_parser

        logger.info("Created a chain")

        return chain
    
    def add_history(self, role, content):
        if role == "character":
            self.input_vars["chat_history"].extend(
                [
                    AIMessage(content=content)
                ]
            )
        elif role == "user":
            self.input_vars["chat_history"].extend(
                [
                    HumanMessage(content=content)
                ]
            )

    def stream(self, input):
        self.input_vars["input"] = input

        result = self.chain.stream(self.input_vars)
        output = ""
        for token in result:
            output += token
            # 한글자씩 스트리밍
            for char in token:
                yield char

        return output

    def stream_streamlit(self, input):
        st.session_state["output"] = ""
        self.input_vars["input"] = input
        container = st.empty()

        retry = 0
        while retry < 5:
            try:
                result = self.chain.stream(self.input_vars)
                for token in result:
                    # 한글자씩 스트리밍
                    for char in token:
                        st.session_state["output"] += char
                        time.sleep(0.01)
                        container.markdown(st.session_state["output"])
                break
            except:
                logger.info(f"{retry}:503ERROR")
                st.session_state["output"] = ""
                retry += 1
                time.sleep(1)
                pass
        
        return st.session_state["output"]

    async def astream(self, input):
        self.input_vars["input"] = input

        result = self.chain.astream(self.input_vars)
        output = ""
        async for token in result:
            output += token 
            # 한글자씩 스트리밍
            for char in token:
                await asyncio.sleep(0.01)
                yield char

    async def astream_streamlit(self, input):
        container = st.empty()
        self.input_vars["input"] = input

        retry = 0
        while retry < 5:
            try:
                async for token in self.chain.astream(self.input_vars):
                    # 한글자씩 스트리밍
                    for char in token:
                        st.session_state["output"] += char
                        await asyncio.sleep(0.1)
                        container.markdown(st.session_state["output"])
                break
            except Exception as e:
                print(e)
                logger.info(f"{retry}:503ERROR")
                st.session_state["output"] = ""
                retry += 1
                await asyncio.sleep(2)
                pass

        return st.session_state["output"]


