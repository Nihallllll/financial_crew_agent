from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.messages import SystemMessage , HumanMessage
from tavily import TavilyClient
from firecrawl import Firecrawl
from dotenv import load_dotenv
load_dotenv()

#model setup
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    
)
# model prompt
prompt = """
You are a Financial Data Analyst Agent. 
Your task is to listen to user queries about stocks, identify the specific company they are referring to, and find its official Stock Ticker Symbol (e.g., Apple -> AAPL, Tesla -> TSLA).

Once you have the ticker symbol, you MUST call the tool `search_stock_data` with the ticker as the argument.

Rules:
1. If the user provides a "nearby name" (e.g., "that electric car company by Musk"), resolve it to the correct ticker (TSLA) before calling the tool.
2. If you are unsure of the ticker, do a quick internal search or ask the user for clarification.
3. Only output the tool call; do not provide a text response until the tool returns the data.
"""

#tools setup
@tool
def search_stock_data(stock_ticker :str) ->dict:
    """Searches the web and market reports for a specific stock ticker.
    
    Args:
        stock_ticker: The stock ticker symbol (e.g., AAPL, TSLA, GOOGL)
    """
    # Standardizing to uppercase for URLs
    ticker = stock_ticker.upper()
    
    # These are high-value URLs where the ticker is the only variable
    search_targets = [
        f"https://finance.yahoo.com/quote/{ticker}",
        f"https://www.marketwatch.com/investing/stock/{ticker}",
        f"https://seekingalpha.com/symbol/{ticker}",
        f"https://www.google.com/finance/quote/{ticker}:NASDAQ" # Or :NYSE
    ]
    query = f"Latest financial report and price analysis for {ticker} stock"
    
    tavily_client = TavilyClient(api_key="")
    response = tavily_client.search(query=query , search_depth="advanced" ,include_domains=search_targets)
    
    return response
    # print(f"Agent is now searching for: {ticker} using targets: {search_targets}")
    # return f"Data for {ticker} retrieved."

agent = create_agent(
    model,
    [search_stock_data],
    system_prompt=SystemMessage(
        content=prompt
    ),
    )


result = agent.invoke({"messages": [HumanMessage("give me analysis of apple stock")]})
final_message = result["messages"][-1]
answer_text = final_message.content[0]["text"]

print(answer_text)