from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
from datetime import datetime

from app.agents.friend_agent import FriendAgent
from app.services.vector_service import VectorService
from app.utils.memory_manager import MemoryManager

app = FastAPI(title="亲友信息智能记忆AI服务", version="1.0.0")

# 初始化服务
vector_service = VectorService()
memory_manager = MemoryManager()
friend_agent = FriendAgent(memory_manager)


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = None


class VectorEmbedRequest(BaseModel):
    original_id: str
    data_type: str  # friend, preference, note
    content: str


class VectorDeleteRequest(BaseModel):
    original_id: str
    data_type: str


class VectorSearchRequest(BaseModel):
    query: str
    top_k: int = 5


@app.get("/")
async def root():
    return {"status": "running", "service": "亲人信息智能记忆AI服务"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """AI对话接口"""
    try:
        response = await friend_agent.chat(
            session_id=request.session_id,
            message=request.message
        )
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vector/embed")
async def embed_vector(request: VectorEmbedRequest):
    """生成并存储向量"""
    try:
        await vector_service.embed_and_store(
            original_id=request.original_id,
            data_type=request.data_type,
            content=request.content
        )
        return {"status": "success", "message": "向量已生成并存储"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vector/delete")
async def delete_vector(request: VectorDeleteRequest):
    """删除向量"""
    try:
        vector_service.delete_vector(
            original_id=request.original_id,
            data_type=request.data_type
        )
        return {"status": "success", "message": "向量已删除"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vector/search")
async def search_vectors(request: VectorSearchRequest):
    """向量搜索"""
    try:
        results = vector_service.search(
            query=request.query,
            top_k=request.top_k
        )
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
