import streamlit as st 
from naraetool.utils import *
import json

setting()

# llm 관련
from pathlib import Path 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from operator import itemgetter

#--------------------------------------------------------------------------
## Settings
#--------------------------------------------------------------------------
session_key = "chat_history"

temp = """\
## INSTRUCTION
- 당신은 배우입니다. 배우의 정보는 INFORMATION을 참고하세요.
- 캐릭터에 몰입해서 말투와 성격을 유지하세요.
- 전에 했던 대화를 반복하지 마세요.
- 너무 짧게 대답하지 마세요.
- INFORMATION 정보 기반으로 INPUT에 답하세요.

## INFORMATION
- NAME: {name}
- GENDER: {gender}
- RELATIONSHIP: {relationship}
- PERSONALITY: {personality}
- DETAILS: {details}
"""

temp_var = {
    "name":"부장님",
    "gender":"여",
    "relationship":"부장님",
    "personality":"까다로움, 날카로움",
    "details": "아이를 좋아함"
}

with st.expander(label=":gear: Settings", expanded=False):
    template = st.text_area(label="Template", value=temp, height=300)
    variable = st.text_area(label="Input_variable", value=temp_var, height=100)
    save_button = st.button(label="Save", use_container_width=True, type="primary")
    if save_button:
        # Chat 인스턴스 생성
        # prompt = PromptTemplate.from_template(template)
        memory = ConversationBufferMemory(
            return_messages=True, 
            memory_key="chat_history"
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", template),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )
        runnable = RunnablePassthrough.assign(
            chat_history = RunnableLambda(memory.load_memory_variables)
            | itemgetter("chat_history")
        )
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        output_parser = StrOutputParser()
        runnable = RunnablePassthrough.assign(
                chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("chat_history")
            )
        chain = runnable | prompt | model | StrOutputParser()
        st.session_state["chain"] = chain
        st.session_state["memory"] = memory
#--------------------------------------------------------------------------
## Load Session Information
#--------------------------------------------------------------------------
if session_key not in st.session_state:
    st.session_state[session_key] = []

if "chain" in st.session_state:
    chain = st.session_state["chain"]
    memory = st.session_state["memory"]
else:
    # Chat 인스턴스 생성
    # prompt = PromptTemplate.from_template(template)
    memory = ConversationBufferMemory(
        return_messages=True, 
        memory_key="chat_history"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )
    runnable = RunnablePassthrough.assign(
        chat_history = RunnableLambda(memory.load_memory_variables)
        | itemgetter("chat_history")
    )
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    output_parser = StrOutputParser()
    runnable = RunnablePassthrough.assign(
            chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("chat_history")
        )
    chain = runnable | prompt | model | StrOutputParser()
    st.session_state["chain"] = chain
    st.session_state["memory"] = memory

#--------------------------------------------------------------------------
## Header & Body
#--------------------------------------------------------------------------
# 첫 채팅을 시작할 때 첫 인사 출력
if len(st.session_state[session_key]) == 0:
    greeting = "안녕하세요.😊"
    st.chat_message("assistant").markdown(greeting)
    st.session_state[session_key].append(
        {"role":"assistant", "content":greeting}
    )

# 채팅 기록이 있을 때 기록된 채팅 출력
else:
    for chat in st.session_state[session_key]:
        st.chat_message(chat["role"]).markdown(chat["content"])

question = st.chat_input(placeholder="메세지 입력")

# 채팅이 입력되었을 때
if question:
    # 입력된 채팅 출력
    st.chat_message("user").markdown(question)
    st.session_state[session_key].append(
        {"role":"user", "content":question}
    )
    
    # 답변 출력
    with st.chat_message("assistant"):
        container = st.empty()
        answer = ""
        var_json = json.loads(variable.replace('\'','\"'))
        var_json["input"] = input
        answer = chain.invoke(var_json)
        st.markdown(answer)
        # for token in chain.stream(var_json):
        #     answer += token
        #     container.markdown(answer)
            
    st.session_state[session_key].append({"role":"assistant", "content":answer})
    # 메모리 저장
    memory.save_context(
        {"inputs": question},
        {"output": answer}
    )

	# 메모리 출력
    print(memory.load_memory_variables({}))