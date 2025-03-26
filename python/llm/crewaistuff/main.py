from crewai import Agent, Task, Crew, Process, LLM

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0
)

researcher = Agent(
    role="{topic} Senior Researcher",
    goal="""Uncover groundbreaking technologies in
    {topic} for year  2024""",
    backstory="""Driven by curiosity, you explore and
    share the latest innovations.""",
    llm=llm
)

research_task = Task(
    description="""Identify the next big trend in
    {topic} with pros and cons.""",
    expected_output="""A 3-paragraph report on emerging
    {topic} technologies.""",
    agent=researcher
)


def main():
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff(inputs={'topic': 'AI Agents'})
    print(result)


if __name__ == "__main__":
    main()
