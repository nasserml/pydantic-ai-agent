# 📈 Stock Price AI Assistant

Welcome to the **Stock Price AI Assistant**! 🎉

This project is a helpful financial assistant that can look up current stock prices through natural language queries. It leverages the power of artificial intelligence with the Pydantic AI Agent, Groq Model, and provides both a command-line and a web interface powered by Gradio.

---

## 🌟 Features

- **Natural Language Interaction**: Ask about stock prices using everyday language.
- **Real-time Stock Data**: Retrieves the latest stock prices using Yahoo Finance.
- **AI-Powered Responses**: Utilizes Pydantic AI and GroqModel for intelligent processing.
- **Web Interface**: User-friendly web application using Gradio.
- **Easy Setup**: Simple installation and configuration steps.

---

## 📋 Table of Contents

- [Demo](#-demo)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
  - [Command-Line Interface](#command-line-interface)
  - [Web Interface](#web-interface)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)




---

## 💻 Installation

Follow these steps to set up the project on your local machine:

1. **Clone the repository**

   ```bash
   git clone https://github.com/nasserml/pydantic-ai-agent.git
   cd pydantic-ai-agent
   ```

2. **Create a virtual environment**

   We recommend using `conda` for managing the virtual environment.

   ```bash
   conda create -p venv python==3.12
   conda activate ./venv
   ```

   Alternatively, you can use `virtualenv`:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🔧 Configuration

Before running the application, you need to configure the environment variables.

1. **Create a `.env` file**

   Copy the `.env.example` file to `.env`:

   ```bash
   cp .env.example .env
   ```

2. **Set your Groq API Key**

   Obtain your Groq API Key from the [Groq Developer Portal](https://groq.com/developers) and update the `.env` file:

   ```env
   GROQ_API_KEY="your_groq_api_key_here"
   ```

   > ⚠️ **Important**: Keep your API Key secure and do not share it publicly.

---

## 🚀 Usage

You can interact with the Stock Price AI Assistant via the command line or through the web interface.

### Command-Line Interface

Run the `app.py` script to interact using the terminal.

```bash
python app.py
```

**Example Scenario:**

The script is pre-configured to ask:

```python
result = stock_agent.run_sync("What is the current price of Apple Inc. (AAPL)?")
```

**Sample Output:**

```
Stock Price: $150.25 USD
Message: The current price of Apple Inc. (AAPL) is $150.25 USD.
```

Feel free to modify the query in `app.py` to ask about different stocks.

### Web Interface

Run the `ui.py` script to launch the Gradio web interface.

```bash
python ui.py
```

**Instructions:**

- After running the script, Gradio will provide you with a local URL (e.g., `http://127.0.0.1:7860`).
- Open the URL in your web browser.
- Enter your query in the text box (e.g., "What is the current price of Tesla stock?").
- Click the **Submit** button to get the response.

---

## 📁 Project Structure

Here's a brief overview of the project files and directories:

```
pydantic-ai-agent/
├── app.py
├── ui.py
├── requirements.txt
├── .env.example
├── commands.txt
└── README.md
```

### Files Description

- **`app.py`**: Command-line application that initializes the AI agent and fetches stock prices based on a user's query.
- **`ui.py`**: Web application using Gradio to provide a user-friendly interface for interacting with the AI assistant.
- **`requirements.txt`**: Lists all Python dependencies required for the project.
- **`.env.example`**: Example environment variables file for configuration.
- **`commands.txt`**: Contains useful commands related to environment setup.
- **`README.md`**: Comprehensive guide and documentation for the project.

---

## 🛠️ Detailed Code Explanation

### `app.py`

```python
from pydantic_ai import Agent
from pydantic import BaseModel
import yfinance as yf
from dotenv import load_dotenv
import os
from pydantic_ai.models.groq import GroqModel

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

model = GroqModel(
    'llama3-groq-70b-8192-tool-use-preview',
    api_key=api_key
)

class StockPriceResult(BaseModel):
    symbol: str
    price: float
    currency: str = "USD"
    message: str

stock_agent = Agent(
    model=model,
    result_type=StockPriceResult,
    system_prompt=(
        "You are a helpful financial assistant that can look up stock prices. "
        "Use the get_stock_price tool to fetch current data."
    ),
)

@stock_agent.tool_plain
def get_stock_price(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info.last_price
    return {
        "price": round(price, 2),
        "currency": "USD"
    }

result = stock_agent.run_sync("What is the current price of Apple Inc. (AAPL)?")

print(f"Stock Price: ${result.data.price:.2f} {result.data.currency}")
print(f"Message: {result.data.message}")
```

**Explanation:**

- **Imports** necessary libraries and loads environment variables.
- **Defines** a `StockPriceResult` model using Pydantic for structured data.
- **Initializes** the AI agent with the specified model and system prompt.
- **Defines** a tool `get_stock_price` that retrieves the current stock price using `yfinance`.
- **Executes** a sample query and prints the result.

### `ui.py`

The `ui.py` script is similar to `app.py` but sets up an asynchronous function for the Gradio interface.

```python
# ... [Same imports and initial setup as app.py] ...

import gradio as gr

# ... [Same model and agent setup as app.py] ...

async def get_stock_info(query):
    try:
        result = await stock_agent.run(query)
        response = f"Stock: {result.data.symbol}\n"
        response += f"Price: ${result.data.price:.2f} {result.data.currency}\n"
        response += f"\n{result.data.message}"
        return response        
    except Exception as e:
        return f"Error: {str(e)}"

demo = gr.Interface(
    fn=get_stock_info,
    inputs=gr.Textbox(
        label="Ask about any stock price",
        placeholder="What is the current price of Apple Inc. (AAPL)?"
    ),
    outputs=gr.Textbox(label="Stock Info"),
    title="Stock Price AI Assistant",
    description="Ask me about any stock price and I'll provide you with the current information.",
)

if __name__ == "__main__":
    demo.launch()
```

**Explanation:**

- **Sets up** a Gradio interface with an asynchronous function `get_stock_info`.
- **Handles** user queries and displays structured responses.
- **Launches** the web application when the script is run.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. **Fork** the Project.
2. **Create** your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. **Commit** your Changes (`git commit -m 'Add some AmazingFeature'`).
4. **Push** to the Branch (`git push origin feature/AmazingFeature`).
5. **Open** a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgements

- 🤖 [Pydantic AI](https://github.com/pydantic/pydantic-ai)
- 🚀 [GroqModel](https://groq.com/)
- 📊 [yfinance](https://pypi.org/project/yfinance/)
- 🌐 [Gradio](https://gradio.app/)
- 📚 [Python Dotenv](https://saurabh-kumar.com/python-dotenv/)
- ❤️ Thanks to all contributors and the open-source community!

---

Feel free to ⭐️ the repository if this project helped you!

For any questions or suggestions, please open an issue or contact me at [mnasserone@gmail.com](mailto:mnasserone@gmail.com).

Happy Coding! 👩‍💻👨‍💻