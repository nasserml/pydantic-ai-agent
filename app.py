from pydantic_ai import Agent
from pydantic import BaseModel
import yfinance as yf
from dotenv import load_dotenv
import os
from pydantic_ai.models.groq import GroqModel

load_dotenv()


api_key = os.getenv("GROQ_API_KEY")

model = GroqModel('llama3-groq-70b-8192-tool-use-preview', api_key='gsk_P**********************')

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

result = stock_agent.run_sync("what is the current price of Apple Inc. (AAPL)?")

print(f"Stock Price: ${result.data.price:.2f} {result.data.currency}")
print(f"Message: {result.data.message}")