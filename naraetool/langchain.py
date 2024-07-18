import os 
from dotenv import load_dotenv 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from operator import itemgetter

def check_api_key(api_name:str) -> None:
    """환경변수에 API가 있는지 확인하는 함수

    Args:
        api_name (str): 확인할 API KEY의 key 값
    """
    load_dotenv()

    if api_name not in os.environ:
        print(f"{api_name} 정보가 없습니다. 확인 후 환경변수에 등록해주세요.")

class Chat:
    def __init__(self, template, input_vars):
        self.template = template
        self.input_vars = input_vars
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
        self.chain = self._make_chain()
        
    def _get_runnable(self):
        runnable = RunnablePassthrough.assign(
            chat_history = RunnableLambda(self.memory.load_memory_variables)
            | itemgetter("chat_history")
        )
        return runnable

    def _get_prompt(self):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ]
        )

        return self.prompt

    def _make_chain(self):
        runnable = self._get_runnable()
        prompt = self._get_prompt()
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        output_parser = StrOutputParser()

        self.chain = runnable | prompt | model | output_parser 

        return self.chain
    
    def invoke(self, input):
        self.input_vars["input"] = input
        output = self.chain.invoke(self.input_vars)

        # print(f"BEFORE: {self.memory}")
        self.memory.save_context(
            {"inputs": input},
            {"outputs": output}
        )
        # print(f"AFTER: {self.memory}")

        return output
    
    def stream(self, input):
        self.input_vars["input"] = input
        output = self.chain.stream(self.input_vars)
        
        # print(f"BEFORE: {self.memory}")
        self.memory.save_context(
            {"inputs": input},
            {"outputs": output}
        )
        # print(f"AFTER: {self.memory}")

        return output

    def stream_st(self, input, container):
        self.input_vars["input"] = input
        output = ""
        for token in self.chain.stream(self.input_vars):
            output += token
            container.markdown(output)

        # print(f"BEFORE: {self.memory}")
        self.memory.save_context(
            {"inputs": input},
            {"outputs": output}
        )
        # print(f"AFTER: {self.memory}")

        return output