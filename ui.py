from pydantic_ai import Agent
from pydantic import BaseModel
import yfinance as yf
from dotenv import load_dotenv
import os
from pydantic_ai.models.groq import GroqModel
import gradio as gr

load_dotenv()


api_key = os.getenv("GROQ_API_KEY")

model = GroqModel('llama3-groq-70b-8192-tool-use-preview', api_key='gsk_P*****************')

class StockPriceResult(BaseModel):
    symbol: str
    price: float
    currency: str = "USD"
    message: str

stock_agent = Agent(
    model=model,
    result_type=StockPriceResult,
    system_prompt="You are a helpful financial assistant that can look up stock price. Use the get_stock_price tool to fetch current data",
)

@stock_agent.tool_plain
def get_stock_price(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info.last_price
    return { "price": round(price, 2), "currency": "USD"}

async def get_stock_info(query):
    try:
        result = await stock_agent.run(query)
        response = f"Stock: {result.data.symbol} \n "
        response += f"Price: ${result.data.price:.2f} {result.data.currency} \n"
        response += f"\n {result.data.message}"
        return response        
    except Exception as e:
        return f"Error: {str(e)}"
        

demo = gr.Interface(
    fn= get_stock_info,
    inputs=gr.Textbox(label="Ask about any stock price", placeholder="What is the current price of Apple Inc. (AAPL)?"),
    outputs=gr.Textbox(label="Stock Info"),
    title="Stock Price AI Assistant",
    description="Ask me about any stock price and I'll provide you with the current information.",
   
)

if __name__ == "__main__":
    demo.launch()