from langchain_core.tools import tool
from typing import List, Dict
from app.services.vector_service import VectorService

_vector_service = VectorService()


async def _semantic_search(query: str, top_k: int = 5) -> List[Dict]:
    """内部方法：返回结构化的检索结果"""
    return await _vector_service.search(query, top_k=top_k)


@tool(description="从向量存储中检索与问题最相关的参考资料")
async def semantic_search(query: str, top_k: int = 5) -> str:
    """语义搜索：在所有数据类型中检索与query最相关的朋友信息记录"""
    results = await _semantic_search(query, top_k=top_k)
    if not results:
        return "未检索到相关记录。"
    return "\n".join(
        f"{i}. [{doc.get('data_type')}] {doc.get('content')} (相似度: {doc.get('similarity')})"
        for i, doc in enumerate(results, 1)
    )
