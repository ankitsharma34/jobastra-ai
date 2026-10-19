from typing import Any

from jobastra_ai.agent.schemas import AgentRequest, AgentResponse

AGENT_RECURSION_LIMIT = 20


class AgentExecutionError(RuntimeError):
    """Raised when the agent cannot complete a request."""


class JobAstraAgentService:
    """Execute independent requests through the JobAstra agent runtime."""

    def __init__(self, agent: Any) -> None:
        self._agent = agent

    async def run(self, request: AgentRequest) -> AgentResponse:
        try:
            result = await self._agent.ainvoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": request.message,
                        }
                    ]
                },
                config={"recursion_limit": AGENT_RECURSION_LIMIT},
            )
            final_message = result["messages"][-1]
            response = final_message.text
            if not isinstance(response, str):
                raise TypeError("Agent response text must be a string")
            return AgentResponse(response=response)
        except AgentExecutionError:
            raise
        except Exception as exc:
            raise AgentExecutionError("The agent could not complete the request") from exc
