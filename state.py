from typing import TypedDict, Annotated
import operator

class FinancialAnalysisState(TypedDict):
    user_query: str
    market_research_data: Annotated[str, operator.add]
    sentiment_data: Annotated[str, operator.add]
    final_report: str
    messages: list

