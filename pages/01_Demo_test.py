import streamlit as st 
from naraetool.utils import *
from naraetool.langchain import *
from naraetool.main_config import configs
from google.api_core import exceptions

setting()

validate_google_api_key()

# 필요한 Config 정의하기
characters = configs.characters
session_keys = configs.session_keys["demo"]
template_name = "Demo1.prompt"
#-------------------------------------------------------------------
# Session state
#-------------------------------------------------------------------
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage,HumanMessage
from langchain_core.output_parsers import StrOutputParser

import asyncio

import asyncio
import streamlit as st

# Mytest 클래스를 정의
class Mytest:
    def __init__(self):
        template = "친구처럼 대답해주세요"
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", template),
                # MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )
        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7
        )
        output_parser = StrOutputParser()
        self.chain = prompt | model | output_parser
    
    async def astream(self, input):
        result = self.chain.astream({"input":input})
        container = st.empty()
        output = ""
        async for token in result:
            # 한글자씩 스트리밍
            for char in token: 
                await asyncio.sleep(0.01)
                output += char
                container.markdown(output)
                print(char, end="", flush=True)

# session_state 초기화
if "chain" not in st.session_state:
    st.session_state["chain"] = None

# 버튼 클릭 시 chain 초기화 및 저장
button = st.button("test")
if button:
    chain = Mytest()
    st.session_state["chain"] = chain

async def run_async_task(input_value):
    chain = st.session_state.get("chain")
    if chain is None:
        st.error("Chain is not initialized.")
        return

    # 비동기 작업 실행
    result = await chain.astream(input_value)
    st.write(result)

# 입력 받기
input_value = st.chat_input(placeholder="메세지를 입력하세요")
if input_value:
    # 실행 중인 이벤트 루프 가져오기
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(run_async_task(input_value))
    else:
        asyncio.run(run_async_task(input_value))



# def init_session(session_keys):
#     for key, value in session_keys.items():
#         # 상태 초기화
#         if key not in st.session_state:
#             st.session_state[key] = value 
#         # page가 바뀌었을 때 상태 초기화
#         elif key == "page" and st.session_state[key] != value:
#             st.session_state = {}
#             st.rerun()

# init_session(session_keys)
# print(st.session_state)

# def start_click():
#     st.session_state["chat_history"] = []
#     st.session_state["is_expand"] = False
#     st.session_state["chat_start"] = True
    
# def make_option(characters):
#     option_dict = {}
#     for key, value in characters.items():
#         name = value["name"]
#         option_dict[name] = key

#     return option_dict 

# def st_add_history(chain, role, content):
#     if role == "character":
#         st.session_state["chat_history"].append(
#             {"role": "assistant", "content": content}
#         )
#     elif role == "user":
#         st.session_state["chat_history"].append(
#             {"role": "user", "content": content}
#         )

#     print(chain.input_vars["chat_history"])
# #-------------------------------------------------------------------
# # Header
# #-------------------------------------------------------------------
# option_dict = make_option(characters)

# with st.expander(
#         label=":gear: Settigns", 
#         expanded=st.session_state["is_expand"]
#     ):  

#     # Prompt Select Box
#     more_text = "➕ 직접 입력"

#     select = st.selectbox(
#         label="PERSONA",
#         options=list(option_dict.keys()) + [more_text]
#     )

#     # Print Template
#     ## 직접 입력을 클릭했을 때 
#     if select == more_text:
#         persona = st.text_area(
#             label="TEMPLATE",
#                 value="",
#                 height=300
#         )
#     ## 기존의 페르소나를 선택했을 때
#     else:
#         key = option_dict[select]
#         key_info = characters[key]
#         persona = read_prompt(key_info["filepath"])
#         persona = st.text_area(
#             label="TEMPLATE",
#             value=persona,
#             height=300,
#             disabled=True
#         )

#         st.session_state["greeting"] = key_info["greeting"]
#         st.session_state["chat_title"] = key_info["name"]
#         st.session_state["description"] = key_info["description"]
        
#     # Chat Start Button
#     start_btn = st.button(
#         label="CHAT START",
#         use_container_width=True,
#         type="primary",
#         on_click=start_click
#     )
    
#     # Chain 재설정
#     if start_btn:
#         input_vars = {
#             "persona": persona,
#             "chat_history": [],
#             "input": ""
#         }
#         chain = Gemini(input_vars, template_name)
#         st.session_state["chain"] = chain
# #-------------------------------------------------------------------
# # Chat Messages
# #-------------------------------------------------------------------
# if st.session_state["chat_start"]:
#     # 채팅 타이틀 출력
#     input_text_align(st.session_state["chat_title"])
#     input_text_align(f"({st.session_state['description']})", font=12)

#     # 주요 변수 불러오기
#     chain = st.session_state["chain"]
#     input_vars = chain.input_vars
#     history = st.session_state["chat_history"]
#     greeting = st.session_state["greeting"]
    
#     # 첫 채팅이 시작되었을 때
#     if len(history) == 0:
#         st.chat_message("assistant").markdown(greeting)
#         st_add_history(chain, role="character", content=greeting)
#     # 채팅 기록이 있을 때
#     else:
#         for chat in st.session_state["chat_history"]:
#             st.chat_message(chat["role"]).markdown(chat["content"])

#     # 채팅창 입력
#     input = st.chat_input(placeholder="메세지를 입력하세요")
#     print("INPUT",input)

#     # 입력 채팅 출력 및 저장
#     st.chat_message("user").markdown(input)
#     st_add_history(chain, role="user", content=input)
    
#     # 답변 출력
#     with st.chat_message("assistant"):
#         retry = 0
#         # API 전송 오류 시 자동 재시도
#         while retry < 5:
#             try:
#                 output = chain.stream_streamlit(input)
#                 break
#             except exceptions.ServiceUnavailable as e:
#                 retry += 1
#         st_add_history(chain, role="character", content=output)
