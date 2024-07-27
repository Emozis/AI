import os 
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage,HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory


def check_api_key(api_name:str) -> None:
    """환경변수에 API가 있는지 확인하는 함수

    Args:
        api_name (str): 확인할 API KEY의 key 값
    """
    load_dotenv()

    if api_name not in os.environ:
        print(f"{api_name} 정보가 없습니다. 확인 후 환경변수에 등록해주세요.")

async def simple_chat(input:str) -> None:
    prompt = PromptTemplate.from_template("{input}에 대해 한국어로 5줄로 설명해줘")
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    output = chain.astream({"input": input})
    result = ""
    async for token in output:
        result += token
        print(token, end="", flush=True)

    return result


class GeminiChain:
    def __init__(
        self,
        user_info=None,
        character_info=None,
        chat_logs=None
    ) -> None:
        
        # 입력값에 대한 변수
        self.inputs = self._get_inputs(user_info, character_info, chat_logs)
        self.memory = ConversationBufferMemory(
            return_messages=True, 
            memory_key="chat_history"
        )

        # 체인에 대한 변수
        self.template_path = "./static/templates/Demo.prompt"
        self.model_name = "gemini-1.5-pro"
        self.temperature = 0.7
        self.chain = self._make_chain()

    def _get_inputs(self, user_info, character_info, chat_logs):
        inputs = {
            "user_info": user_info,
            "character_info" : character_info,
            "chat_history": self._get_chat_logs(chat_logs)
        }

        return inputs

    def _get_chat_logs(self, chat_logs):
        if not chat_logs:
            return []

        chat_history = []
        for log in chat_logs:
            if log["role"] == "user":
                chat = HumanMessage(log["contents"])
            else:
                chat = AIMessage(log["contents"])
            
        return chat_history.append(chat)
    
    @staticmethod
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
    
    def _get_prompts(self):
        # 프롬프트 설정
        template = self.read_prompt(self.template_path)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", template),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        return prompt
    
    def _make_chain(self):
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

        return chain

    def _save_memory(self, input, output):
            self.memory.save_context(
            {"inputs": input},
            {"output": output}
        )

    async def astream(self, input):
        self.inputs["input"] = input

        output = ""
        result = self.chain.astream(self.inputs)
        async for token in result:
            output += token 
            # 소켓 통신 코드 
            # 테스트 코드
            print(token, end="", flush=True)
        
        # 메모리에 저장
        self._save_memory(input, output)
        
        return output
        