from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.messages import SystemMessage , HumanMessage
from tavily import TavilyClient
from firecrawl import Firecrawl
from dotenv import load_dotenv
import os
load_dotenv()

#model initialization
model= ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.1
)

# prompt

prompt ="""
### ROLE
You are a Senior Financial Intelligence Agent. Your goal is to provide real-time, data-driven insights on stocks by searching the web, social media, and financial news hubs.

### TASK
When a user asks about a company, a sector, or a specific stock (even if they use a "nearby name" or informal description):
1. **Identify the Ticker:** Resolve the company name to its official 1-5 letter Stock Ticker Symbol (e.g., "The iPhone company" -> AAPL).
2. **Call the Tool:** You MUST call the `get_all_stock_links` function using the identified ticker.
3. **Gather All News:** Explicitly instruct the tool to fetch data from ALL categories: Latest News, Social Sentiment (Tweets/Stocktwits), and Financial Reports.

### TOOL CALLING PROTOCOL
- Do NOT guess or use your internal training data for current prices or news.
- ALWAYS call `get_all_stock_links  (stock_ticker="TICKER")` as the very first step.
- If the user query is vague (e.g., "What's happening with AI chips?"), identify the primary leaders (e.g., NVDA, AMD) and call the tool for the most relevant one.

### OUTPUT REQUIREMENTS
Once the tool returns the data, synthesize it into a report with these sections:
- 🟢 **Market Pulse:** Current price and immediate trend.
- 📰 **Top Headlines:** Summary of the most recent 3-5 news articles.
- 💬 **Social Sentiment:** Summary of recent "tweets" and community discussion from Stocktwits/X.
- ⚠️ **Key Risks/Updates:** Any upcoming earnings or red flags found in reports.
"""

@tool
def get_all_stock_links(stock_ticker):
    """
    Called by the LLM. 
    Constructs specific URLs and uses a search tool (Tavily/Firecrawl) 
    to scrape news, tweets, and financials.
    """
    ticker = stock_ticker.upper()
    
    # Organize by Category
    links = [
        f"https://finance.yahoo.com/quote/{ticker}",
        f"https://www.google.com/finance/quote/{ticker}:NASDAQ",
        f"https://stocktwits.com/symbol/{ticker}",
        f"https://seekingalpha.com/symbol/{ticker}/analysis",
        f"https://x.com/search?q=%24{ticker}&f=live"
    ]
    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))
    # Scrape a website:
    scrape_result = firecrawl.batch_scrape(links, formats=['summary'])
    #You can now pass these specific URLs to Firecrawl for scraping
    return scrape_result

agent = create_agent(
    model=model , 
    tools=[get_all_stock_links],
    system_prompt=SystemMessage(
        content=prompt
    )
    )

result = agent.invoke({"messages": [HumanMessage("give me analysis of apple stock")]})

# Extract and print just the final AI response
for message in result['messages']:
    if hasattr(message, 'content') and message.content and 'Market Pulse' in message.content:
        print("\n" + "="*80)
        print("APPLE STOCK ANALYSIS")
        print("="*80)
        print(message.content)
        print("="*80)