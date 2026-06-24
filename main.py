from graph import build_graph

def main():
    print("Initializing QA Test Selector Agent...")
    app = build_graph()
    
    print("Agent ready. Type 'exit' to quit.\n")
    
    while True:
        user_query = input("Developer Query: ")
        if user_query.lower() in ['exit', 'quit']:
            break
            
        print("\nThinking (Extracting component -> Querying Neo4j -> Synthesizing plan)...\n")
        
        initial_state = {"user_input": user_query}
        output = app.invoke(initial_state)
        
        print("--- Testing Plan ---")
        print(output["final_response"])
        print("-" * 20 + "\n")

if __name__ == "__main__":
    main()