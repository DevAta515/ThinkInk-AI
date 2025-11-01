from fastapi import FastAPI, Request
from src.graphs.graphbuilder import GraphBuilder
from src.llms.groqllm import GroqLLM
import uvicorn
from fastapi.responses import JSONResponse
from datetime import datetime

import os
from dotenv import load_dotenv
load_dotenv()

app=FastAPI()
os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

@app.get("/")
async def root():
    return {"message": "ThinkInk-AI Blog Generator API"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API status
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "ThinkInk-AI Blog Generator",
            "version": "1.0.0"
        }
    )

@app.post("/blogs")
async def create_blogs(request:Request):
    data =await request.json()
    topic=data.get("topic","")
    language=data.get("language","")

    llm=GroqLLM().get_llm()

    graph_builder=GraphBuilder(llm)

    if topic and language:
        graph=graph_builder.setup_graph(usecase="Topic with Translation")
        state=graph.invoke({"topic":topic, "curr_lang":language})
    elif topic:
        graph=graph_builder.setup_graph(usecase="Topic")
        state=graph.invoke({"topic":topic})

    return {"data":state}
    

if __name__=="__main__":
    uvicorn.run("app:app",host="0.0.0.0", port=8080, reload=True)