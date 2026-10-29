import os

from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, AIMessage

from app.config import CHAT_MODEL, QWEN_API_KEY
from app.utils.memory_manager import MemoryManager
from app.tools.query_tools import (
    get_friend_detail,
    get_friend_likes,
    get_friend_dislikes,
    get_friend_notes,
    get_all_friends_brief,
    get_friend_summary,
)
from app.tools.search_tools import semantic_search
from app.tools.birthday_tools import get_birthday_info, get_current_time
from app.prompts.main_prompt import SYSTEM_PROMPT

# 设置DashScope API密钥（ChatTongyi通过此环境变量读取密钥）
os.environ["DASHSCOPE_API_KEY"] = QWEN_API_KEY


class FriendAgent:
    """朋友信息智能Agent - 基于LangChain create_agent的ReAct自主决策Agent

    不再需要人工意图检测和工具编排，Agent自主遵循「思考→行动→观察→再思考」
    流程判断何时调用工具、调用哪些工具，最终生成回答。
    """

    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager

        # 初始化通义千问聊天模型
        self.llm = ChatTongyi(model=CHAT_MODEL, temperature=0.7)

        # 使用create_agent创建自主决策的ReAct Agent
        # Agent内部会自动绑定工具、构建推理循环，不需要外部编排
        self.agent = create_agent(
            model=self.llm,
            system_prompt=SYSTEM_PROMPT,
            tools=[
                semantic_search,
                get_friend_detail,
                get_friend_likes,
                get_friend_dislikes,
                get_friend_notes,
                get_all_friends_brief,
                get_friend_summary,
                get_birthday_info,
                get_current_time,
            ],
        )

    async def chat(self, session_id: str, message: str) -> str:
        """处理用户对话：
        1. 获取对话历史并转为LangChain消息格式
        2. 交由Agent自主判断是否需要调用工具、调用哪些工具
        3. Agent自动执行ReAct循环直至生成最终回答
        4. 保存对话历史
        """
        # 1. 获取对话历史
        history = self.memory_manager.get_history(session_id)

        # 2. 转为LangChain消息格式
        messages = []
        for msg in history:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))

        # 3. 追加当前用户消息
        messages.append(HumanMessage(content=message))

        # 4. 执行Agent自主决策（ReAct循环）
        # Agent自动判断：是否需要调用工具 → 调用哪些工具 → 观察结果 → 再思考 → 最终回答
        response_text = ""
        try:
            async for chunk in self.agent.astream(
                {"messages": messages},
                stream_mode="values",
            ):
                latest = chunk["messages"][-1]
                if hasattr(latest, "content") and latest.content:
                    response_text = latest.content.strip()
        except Exception as e:
            print(f"Agent execution error: {e}")
            response_text = "AI服务暂时不可用，请稍后重试。"

        # 5. 保存对话历史
        self.memory_manager.add_to_history(session_id, "user", message)
        self.memory_manager.add_to_history(session_id, "assistant", response_text)

        return response_text
