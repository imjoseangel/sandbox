import asyncio

from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
)

from llama_index.utils.workflow import (
    draw_all_possible_flows,
    draw_most_recent_execution,
)

# `pip install llama-index-llms-ollama` if you don't already have it
from llama_index.llms.ollama import Ollama


class JokeEvent(Event):
    joke: str


class JokeFlow(Workflow):
    llm = Ollama(model="gemma2:latest", request_timeout=120.0)

    @step
    async def generate_joke(self, ev: StartEvent) -> JokeEvent:
        topic = ev.topic

        prompt = f"Write your best joke about {topic}."
        response = await self.llm.acomplete(prompt)
        return JokeEvent(joke=str(response))

    @step
    async def critique_joke(self, ev: JokeEvent) -> StopEvent:
        joke = ev.joke

        prompt = f"Give a thorough analysis and critique of the following joke: {joke}"
        response = await self.llm.acomplete(prompt)
        return StopEvent(result=str(response))


async def main():
    # Draw all
    draw_all_possible_flows(JokeFlow(), filename="joke_flow_all.html")

    w = JokeFlow(timeout=60, verbose=False)
    result = await w.run(topic="cats")
    print(str(result))
    draw_most_recent_execution(w, filename="joke_flow_recent.html")

if __name__ == "__main__":
    asyncio.run(main())
