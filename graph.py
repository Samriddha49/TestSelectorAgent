import os
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from google import genai
from database import fetch_impacted_tests
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 1. Define State
class AgentState(TypedDict):
    user_input: str
    component_name: Optional[str]
    retrieved_data: Optional[str]
    final_response: Optional[str]

# 2. Define Nodes
def extract_component_node(state: AgentState) -> AgentState:
    prompt = f"""
    You are an AI that extracts software component names from user queries.
    Available components in the system: 'AuthService', 'UserProfileUI', 'EmailDispatcher', 'TokenValidator'.
    
    User Query: "{state['user_input']}"
    
    Return ONLY the exact component name from the list above. If none match, return 'None'.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    component = response.text.strip()
    return {"component_name": component if component != "None" else None}

def database_retrieval_node(state: AgentState) -> AgentState:
    component = state.get("component_name")
    graph_data = fetch_impacted_tests(component)
    return {"retrieved_data": graph_data}

def synthesize_response_node(state: AgentState) -> AgentState:
    prompt = f"""
    You are an expert QA Orchestration Assistant. 
    The developer asked: "{state['user_input']}"
    
    Here is the exact impact scope retrieved from the Neo4j dependency graph:
    \"\"\"
    {state['retrieved_data']}
    \"\"\"
    
    Formulate a clear response explaining which business scenarios are impacted and list the specific Test Cases they must execute. 
    Keep it professional, concise, and easy to read. Do not hallucinate test cases not listed in the data.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    return {"final_response": response.text}

# 3. Build and Compile Graph
def build_graph():
    builder = StateGraph(AgentState)
    
    builder.add_node("extractor", extract_component_node)
    builder.add_node("retriever", database_retrieval_node)
    builder.add_node("synthesizer", synthesize_response_node)
    
    builder.add_edge(START, "extractor")
    builder.add_edge("extractor", "retriever")
    builder.add_edge("retriever", "synthesizer")
    builder.add_edge("synthesizer", END)
    
    return builder.compile()