import streamlit as st 
from naraetool.utils import *

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

def read_isfj(x):
    isfj_path = Path("./docs/isfj.txt")
    return isfj_path.read_text(encoding="utf-8")

template = """\
# INSTRUCTION
- 당신의 MBTI는 ISFJ입니다. 
- 당신의 성격은 PERSONALITY와 같습니다.
- PERSONALITY에 맞춰 USER에 답변하세요.

# PERSONALITY: {personality}

# USER: {input}
"""
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
    runnable1 = {"input": RunnablePassthrough()}
    runnable2 = RunnablePassthrough.assign(
            chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("chat_history"),
            personality=RunnableLambda(read_isfj)
        )
    runnable = runnable1 | runnable2
    chain = runnable | prompt | model | StrOutputParser()
    st.session_state["chain"] = chain
    st.session_state["memory"] = memory

#--------------------------------------------------------------------------
## Header & Body
#--------------------------------------------------------------------------
# 첫 채팅을 시작할 때 첫 인사 출력
if len(st.session_state[session_key]) == 0:
    greeting = "안녕하세요. 제 MBTI는 ISFJ입니다.😊"
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
        for token in chain.invoke(question):
            answer += token
            container.markdown(answer)
            
    st.session_state[session_key].append({"role":"assistant", "content":answer})
    # 메모리 저장
    memory.save_context(
        {"inputs": question},
        {"output": answer}
    )

	# 메모리 출력
    print(memory.load_memory_variables({}))