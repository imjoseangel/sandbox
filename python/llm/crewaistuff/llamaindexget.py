
import os
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from crewai_tools import LlamaIndexTool
from crewai import Agent, Task, Crew, LLM


reader = SimpleDirectoryReader(input_files=["uber_10k.pdf"])
docs = reader.load_data()

llm = Gemini(
    model_name="models/gemini-2.0-flash",
    api_key=os.environ["GEMINI_API_KEY"]
)

crewaillm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0
)


Settings.embed_model = GeminiEmbedding(
    model_name="models/embedding-001",
    api_key=os.environ["GEMINI_API_KEY"]
)


index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine(similarity_top_k=5, llm=llm)

# try out query engine tool

query_tool = LlamaIndexTool.from_query_engine(
    query_engine,
    name="Uber 2019 10K Query Tool",
    description="Use this tool to lookup the 2019 Uber 10K Annual Report",
)

print(query_tool.args_schema.schema())

# Define your agents with roles and goals
researcher = Agent(
    role="Senior Financial Analyst",
    goal="Uncover insights about different tech companies",
    backstory="""You work at an asset management firm.
    Your goal is to understand tech stocks like Uber.""",
    verbose=True,
    allow_delegation=False,
    tools=[query_tool],
    llm=crewaillm
)
writer = Agent(
    role="Tech Content Strategist",
    goal="Craft compelling content on tech advancements",
    backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives.""",
    verbose=True,
    allow_delegation=False,
    llm=crewaillm
)

# Create tasks for your agents
task1 = Task(
    description="""Conduct a comprehensive analysis of Uber's risk factors in 2019.""",
    expected_output="Full analysis report in bullet points",
    agent=researcher,
)

task2 = Task(
    description="""Using the insights provided, develop an engaging blog
    post that highlights the headwinds that Uber faces.
    Your post should be informative yet accessible, catering to a casual audience.
    Make it sound cool, avoid complex words.""",
    expected_output="Full blog post of at least 4 paragraphs",
    agent=writer,
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=True,
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)
