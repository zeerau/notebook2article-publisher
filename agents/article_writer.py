from crewai import Agent
from langchain_community.chat_models import ChatOpenAI

def ArticleWriterAgent():
    return Agent(
        role="Technical Writer",
        goal="Write a LinkedIn-style article with an introduction, clear sections, and a conclusion, making complex code and concepts accessible and engaging for beginners.",
        backstory="You are a technical writer who specializes in transforming technical content into engaging, structured, and beginner-friendly articles for a broad audience.",
        llm=ChatOpenAI(temperature=0.7, max_tokens=2048),
        verbose=True
    )
