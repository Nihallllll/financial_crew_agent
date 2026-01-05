# from tavily import TavilyClient
# from firecrawl import Firecrawl

# # tavily_client = TavilyClient(api_key="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")
# # response = tavily_client.search("Tell me the detailed research on hyundai stock in indian , also tell me which wenbsites did you used")

# # print(response)

#  
# # #https://www.investing.com/search/?q=Hyundai


# firecrawl = Firecrawl(api_key="fc-9f7306e415e146e0acb291bc6923956f")
# # Scrape a website:
# scrape_result = firecrawl.scrape('https://www.investing.com/search/?q=Hyundai', formats=['markdown', 'html'])
# print(scrape_result)

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature = 0.1
)

print(model.invoke("what is todays date").content)