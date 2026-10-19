from collections.abc import Sequence
from typing import Any

from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool

from jobastra_ai.agent.prompts import JOB_ASTRA_AGENT_SYSTEM_PROMPT


def create_jobastra_agent(
    model: BaseChatModel,
    tools: Sequence[BaseTool],
) -> Any:
    """Create the JobAstra agent from preconfigured runtime dependencies."""

    return create_agent(
        model=model,
        tools=tools,
        system_prompt=JOB_ASTRA_AGENT_SYSTEM_PROMPT,
    )
