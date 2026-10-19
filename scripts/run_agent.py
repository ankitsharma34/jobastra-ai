import argparse
import asyncio
from pathlib import Path

from pydantic import ValidationError

from jobastra_ai.agent import (
    AgentExecutionError,
    AgentRequest,
    JobAstraAgentService,
    create_jobastra_agent,
)
from jobastra_ai.applications.service import ApplicationAnswerService
from jobastra_ai.career.schemas import CareerProfile
from jobastra_ai.jobs.service import JobDescriptionService
from jobastra_ai.knowledge.store import get_vector_store
from jobastra_ai.llm.config import get_llm_settings
from jobastra_ai.llm.models import get_chat_model
from jobastra_ai.llm.services import LLMService
from jobastra_ai.matching.service import JobMatchingService
from jobastra_ai.rag.retriever import CareerRetriever
from jobastra_ai.tools import create_agent_tools


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the local JobAstra agent",
        epilog=(
            "Windows CMD example:\n"
            "  uv run python scripts/run_agent.py --user-id user-123 "
            '--profile career-profile.json --message "Analyze this job"\n\n'
            "Create your private career-profile.json from career-profile.example.json.\n"
            "Omit --profile to choose a file or use indexed career evidence only."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--user-id", help="User ID whose indexed career evidence is available")
    parser.add_argument(
        "--profile",
        type=Path,
        help="Path to your private CareerProfile JSON file",
    )
    parser.add_argument("--message", help="Message to send instead of prompting interactively")
    return parser.parse_args()


def load_profile(path: Path) -> CareerProfile:
    if not path.is_file():
        raise FileNotFoundError(
            f"Career profile file not found: {path.resolve()}. "
            "Copy career-profile.example.json to career-profile.json and add your details, "
            "or provide an existing file with --profile."
        )
    return CareerProfile.model_validate_json(path.read_text(encoding="utf-8"))


def resolve_profile(path: Path | None) -> CareerProfile:
    if path is not None:
        return load_profile(path)

    while True:
        value = input(
            "Career profile JSON path "
            "(optional; press Enter to use indexed evidence only; "
            "template: career-profile.example.json): "
        ).strip()
        if not value:
            print("Using indexed career evidence without a local profile file.")
            return CareerProfile()
        try:
            return load_profile(Path(value))
        except (OSError, ValidationError) as exc:
            print(f"Could not load career profile: {exc}")


async def run() -> None:
    args = parse_args()
    user_id = (args.user_id or input("User ID: ")).strip()
    if not user_id:
        raise ValueError("User ID must not be empty")

    profile = resolve_profile(args.profile)

    message = (args.message or input("You: ")).strip()
    if not message:
        raise ValueError("Message must not be empty")

    model = get_chat_model()
    llm_service = LLMService(
        model=model,
        settings=get_llm_settings(),
    )
    retriever = CareerRetriever(get_vector_store())
    job_service = JobDescriptionService(llm_service)
    matching_service = JobMatchingService(llm_service, retriever)
    application_service = ApplicationAnswerService(retriever, llm_service)
    tools = create_agent_tools(
        user_id=user_id,
        career_profile=profile,
        career_retriever=retriever,
        job_service=job_service,
        matching_service=matching_service,
        application_service=application_service,
    )
    agent = create_jobastra_agent(model, tools)
    response = await JobAstraAgentService(agent).run(AgentRequest(message=message))

    print(f"\nJobAstra:\n{response.response}")


def main() -> None:
    try:
        asyncio.run(run())
    except AgentExecutionError:
        raise SystemExit(
            "Error: The agent could not complete the request. "
            "Check the configured LLM API key, quota, and rate limits, then retry."
        ) from None
    except (OSError, ValidationError, ValueError) as exc:
        raise SystemExit(f"Error: {exc}") from None


if __name__ == "__main__":
    main()
