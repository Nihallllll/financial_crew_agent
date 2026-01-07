from graph import create_agent_graph
def analyze_stock(query: str):
    """Main function to run the financial analysis pipeline"""
    graph = create_agent_graph()
    
    initial_state = {
        "user_query": query,
        "market_research_data": "",
        "sentiment_data": "",
        "final_report": "",
        "messages": []
    }
    
    print(f"\n{'='*80}")
    print(f"Starting Financial Analysis for: {query}")
    print(f"{'='*80}\n")
    
    # Run the graph
    result = graph.invoke(initial_state)
    
    print(f"\n{'='*80}")
    print("FINAL FINANCIAL REPORT")
    print(f"{'='*80}\n")
    print(result["final_report"])
    print(f"\n{'='*80}\n")
    
    return result

# Example usage
if __name__ == "__main__":
    analyze_stock("Give me analysis of Apple stock")