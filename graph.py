from state import FinancialAnalysisState
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain.messages import HumanMessage
from market_research_agent import research_agent
from market_sentiment_agent import sentiment_agent
from report_writer_agent import report_writer_agent
def create_agent_graph():
    workflow = StateGraph(FinancialAnalysisState)

    #N0DES
    workflow.add_node("market_research", research_agent)
    workflow.add_node("sentiment_analysis" , sentiment_agent)
    workflow.add_node("report_writer", report_writer_agent)

    workflow.set_entry_point("market_research")
    workflow.set_entry_point("sentiment_analysis")

    workflow.add_edge("market_research" , "report_writer")
    workflow.add_edge("sentiment_analysis","report_writer")
    workflow.add_edge("report_writer",END)

    return workflow.compile()