# notebook2article-publisher

This project uses CrewAI agents to read a Jupyter notebook, generate a detailed beginner-friendly article explaining the code and concepts, and publish it to LinkedIn via Make.com.

## Features
- Reads local Jupyter notebook files (.ipynb)
- Summarizes and explains code and markdown cells
- Writes engaging LinkedIn-style articles
- Publishes articles automatically via Make.com webhook

## Usage
1. Clone the repo and set up your Python environment.
2. Add your OpenAI API key and Make.com webhook URL to a `.env` file.
3. Run `main.py` and follow the prompt to select your notebook file.
4. The generated article will be posted to LinkedIn via Make.com.

## Setup
```bash
pip install -r requirements.txt
```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `MAKE_WEBHOOK_URL`: Your Make.com webhook URL

## Example .env
```
OPENAI_API_KEY=sk-...
MAKE_WEBHOOK_URL=https://hook.eu2.make.com/xxxxxx
```

## License
MIT
