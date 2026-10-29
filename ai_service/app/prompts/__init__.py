from app.prompts.templates import (
    GENERAL_QUERY_TEMPLATE,
    BIRTHDAY_QUERY_TEMPLATE,
    PREFERENCE_QUERY_TEMPLATE,
    DISLIKE_QUERY_TEMPLATE,
    SUMMARY_QUERY_TEMPLATE,
    NOTE_QUERY_TEMPLATE,
    UPCOMING_BIRTHDAY_TEMPLATE,
    INTENT_PROMPT_MAP,
    get_prompt_template,
    format_retrieved_context,
    format_tool_results,
)
from app.prompts.main_prompt import SYSTEM_PROMPT

__all__ = [
    "GENERAL_QUERY_TEMPLATE",
    "BIRTHDAY_QUERY_TEMPLATE",
    "PREFERENCE_QUERY_TEMPLATE",
    "DISLIKE_QUERY_TEMPLATE",
    "SUMMARY_QUERY_TEMPLATE",
    "NOTE_QUERY_TEMPLATE",
    "UPCOMING_BIRTHDAY_TEMPLATE",
    "INTENT_PROMPT_MAP",
    "get_prompt_template",
    "format_retrieved_context",
    "format_tool_results",
    "SYSTEM_PROMPT",
]
