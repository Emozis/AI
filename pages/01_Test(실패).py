import streamlit as st 
from naraetool.langchain import *
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
page_title = "test"

# Set Seesion Keys
key_option_btn = f"option_btn_{page_title}"
key_chat_history = f"chat_history_{page_title}"
key_chat = f"chain_{page_title}"

# Event Functions
def expand(state):
    st.session_state[key_option_btn] = state

# Etc
template = """
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

input_vars = {
    "name": "아무개",
    "gender": "남",
    "relationship": "사수",
    "personality": "예민함, 반말함, 말을 꼬아서 함",
    "details": "싸가지없음"
}
#--------------------------------------------------------------------------
## Load Session Information
#--------------------------------------------------------------------------
if key_option_btn not in st.session_state:
    st.session_state[key_option_btn] = True
if key_chat_history not in st.session_state:
    st.session_state[key_chat_history] = []

if key_chat in st.session_state:
    memory, chain = st.session_state[key_chat]
else:
    memory, chain = make_chain(template)
    st.session_state[key_chat] = (memory, chain)
    
#--------------------------------------------------------------------------
## Option Container
#--------------------------------------------------------------------------
with st.expander(label=":gear: Settings", expanded=st.session_state[key_option_btn]):
    name = st.text_input(label="Name", value=input_vars["name"])
    col_left, col_right = st.columns(2)
    with col_left:
        gender = st.radio(
            label="Gender",
            options=["남", "여"],
            horizontal=True
        )
    with col_right:
        relationship = st.selectbox(
            label="Relationship",
            options=["-", "직장동료", "가족", "친구", "직접 입력"]
        )
        if relationship == "직접 입력":
            relationship = st.text_input(
                label="Relationship", 
                label_visibility="collapsed"
            )

    personality = st.text_input(
        value=input_vars["personality"],
        label="Personality"
    )
    details = st.text_area(
        value=input_vars["details"],
        label="Details", 
        height=100
    )

    template = st.text_area(
        value=template,
        label="Template", 
        height=300
    )

    input_vars = {
        "name": name,
        "gender": gender,
        "relationship": relationship,
        "personality": personality,
        "details": details
    }

    submit = st.button(
        label="Save",
        use_container_width=True,
        type="primary",
        on_click=expand,
        args=[False]
    )

    if submit:
        st.session_state[key_chat_history] = []
        memory, chain = make_chain(template)
        st.session_state[key_chat] = (memory, chain)
#--------------------------------------------------------------------------
## Chatting
#--------------------------------------------------------------------------
if st.session_state[key_chat_history] == []:
    greeting = f"안녕하세요. 제 이름은 {input_vars['name']}입니다. 😊"
    st.chat_message("assistant").markdown(greeting)
    st.session_state[key_chat_history].append(
        {"role":"assistant", "content":greeting}
    )
else:
    for history in st.session_state[key_chat_history]:
        st.chat_message(history["role"]).markdown(history["content"])

question = st.chat_input(placeholder="메세지 입력")

if question:
    st.chat_message("user").markdown(question)
    st.session_state[key_chat_history].append(
        {"role":"user", "content":question}
    )

    with st.chat_message("assistant"):
        
        with st.spinner(text="Loading..."):
            container = st.empty()
            input_vars["input"] = question
            
            answer = chain.invoke(input_vars)
            st.markdown(answer)
            # answer = ""
            # for token in chain.stream(input_vars):
            #     answer += token
            #     container.markdown(answer)
        
        memory.save_context(
            {"inputs": question},
            {"outputs": answer}
        )

        st.session_state[key_chat_history].append(
            {"role":"assistant", "content":answer}
        )

    print(memory.load_memory_variables({}))
print("="*100)
# print(chain.chain)

        

        