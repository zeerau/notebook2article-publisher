

import os
from dotenv import load_dotenv
from crewai import Crew
from agents.code_reader import CodeReaderAgent
from agents.article_writer import ArticleWriterAgent
from utils.notebook_parser import extract_notebook_code_and_markdown
from publishers.linkedin_via_make import post_to_linkedin_via_make

# Load environment variables
load_dotenv()

# Prompt user for notebook file
notebook_path = input("Enter the path to your Jupyter notebook (.ipynb): ").strip()
if not os.path.isfile(notebook_path) or not notebook_path.endswith(".ipynb"):
    print("❌ Invalid notebook file.")
    exit()
print(f"[📘] Processing notebook: {notebook_path}")

# Extract notebook content
code, markdown, ordered_cells = extract_notebook_code_and_markdown(notebook_path)

# Format ordered cells for LLM prompt
def format_cells_for_prompt(ordered_cells):
    formatted = []
    for i, cell in enumerate(ordered_cells, 1):
        if cell["type"] == "markdown":
            formatted.append(f"Markdown Cell {i}:\n{cell['content']}\n")
        else:
            formatted.append(f"Code Cell {i}:\n{cell['content']}\n")
    return "\n".join(formatted)

formatted_cells = format_cells_for_prompt(ordered_cells)

# Setup CrewAI agents
code_agent = CodeReaderAgent()
writer_agent = ArticleWriterAgent()

# Step 1: Run code reader agent
crew_code = Crew(
    agents=[code_agent],
    tasks=[
        {
            "agent": code_agent,
            "description": "Step-by-step walkthrough and explanation of each notebook cell, matching cell order.",
            "expected_output": "A numbered, structured summary with clear explanations for each code and markdown cell, following the notebook's flow.",
            "task": (
                "You are an expert Python educator. For each cell in the notebook below:\n"
                "- If it is a code cell, explain step-by-step what the code does, why it is written this way, and how it contributes to the notebook's goal.\n"
                "- If it is a markdown cell, summarize the main point or context it provides.\n"
                "Number your explanations to match the cell order. Be clear, concise, and beginner-friendly.\n"
                "Here are the notebook cells:\n\n"
                f"{formatted_cells}"
            )
        }
    ]
)
results_code = crew_code.kickoff()
if hasattr(results_code, "model_dump"):
    code_dict = results_code.model_dump()
    code_reader_output = code_dict.get('raw')
    if not code_reader_output or not isinstance(code_reader_output, str):
        tasks_output = code_dict.get('tasks_output')
        if tasks_output and isinstance(tasks_output, list) and len(tasks_output) > 0:
            code_reader_output = tasks_output[0].get('output')
    if not code_reader_output or not isinstance(code_reader_output, str):
        raise Exception("Could not extract code reader output from CrewAI output.")
else:
    raise Exception("Cannot extract code reader output from CrewOutput. See printed results for structure.")

# Step 2: Run article writer agent with code_reader_output
crew_article = Crew(
    agents=[writer_agent],
    tasks=[
        {
            "agent": writer_agent,
            "description": "Write a LinkedIn-style article with intro, sections, and conclusion, based on the structured summary.",
            "expected_output": "A well-structured, engaging LinkedIn article with introduction, clear sections, and a conclusion, accessible to beginners.",
            "task": (
                "Write a detailed, engaging LinkedIn article based on the structured summary below.\n"
                "- Start with an introduction to the notebook's main concept.\n"
                "- For each step, explain the code and concepts in a way that is accessible to beginners.\n"
                "- Use clear headings and sections.\n"
                "- Conclude with key takeaways or practical applications.\n"
                "Here is the structured summary:\n\n"
                f"{code_reader_output}"
            )
        }
    ]
)
results_article = crew_article.kickoff()
if hasattr(results_article, "model_dump"):
    article_dict = results_article.model_dump()
    article = article_dict.get('raw')
    if not article or not isinstance(article, str):
        tasks_output = article_dict.get('tasks_output')
        if tasks_output and isinstance(tasks_output, list) and len(tasks_output) > 0:
            article = tasks_output[0].get('output')
    if not article or not isinstance(article, str):
        raise Exception("Could not extract article text from CrewAI output.")
else:
    raise Exception("Cannot extract article from CrewOutput. See printed results for structure.")

# Use the first markdown cell as the title if available
if markdown and len(markdown) > 0:
    title = markdown[0].splitlines()[0].strip("# ").strip()
else:
    title = "📘 Learn Python from a Real Notebook Example"
print(f"[✅] Article created:\n{title}\n\n{article[:300]}...")


# Publish the entire article as a single LinkedIn post
post_to_linkedin_via_make(title, article)
print("✅ Posted article to LinkedIn.")