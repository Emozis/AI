# uvicorn main:app --host 0.0.0.0 --port 8080 --reload
import uvicorn
import asyncio
import json
from dotenv import load_dotenv 
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from naraetool.langchain import *


check_api_key("GOOGLE_API_KEY")

app = FastAPI() 

@app.get("/")
def root():
    return {"Hello": "Python"}

@app.get("/test")
async def chatbot():
    chain = GeminiChain()

    # astream 메서드 호출
    input_text = "python에 대해 3줄로 알려줄래?"
    output = await chain.astream(input_text)

    content = {"result": output}

    return JSONResponse(content=content, media_type="application/json; charset=utf-8")


@app.get("/simple_test")
async def simple():
    output = await simple_chat("python")

    content = {"result": output}

    # Response(content=json.dumps(content), media_type="application/json; charset=utf-8")
    return JSONResponse(content=content, media_type="application/json; charset=utf-8")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)