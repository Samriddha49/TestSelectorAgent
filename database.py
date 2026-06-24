import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

def fetch_impacted_tests(component_name: str) -> str:
    """Queries Neo4j for scenarios and tests linked to a component."""
    if not component_name:
         return "No recognizable component found."

    # properties(t) grabs ALL data in the node, ignoring strict key names
    query = """
    MATCH (c:Component {Component_Name: $name})-[:Participates_in]->(s:Scenario)-[:Covered_by]->(t:TestCase)
    RETURN s.Scenario_Name AS Scenario, collect(properties(t)) AS Tests
    """
    
    try:
        with GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD)) as driver:
            records, _, _ = driver.execute_query(query, name=component_name)
            
            if not records:
                return f"No testing paths found for component: {component_name}"
                
            results = []
            for record in records:
                scenario = record["Scenario"]
                test_strings = []
                
                for t in record["Tests"]:
                    # Safely fallback through the possible capitalizations the UI might have used
                    t_id = t.get('Test_Case_ID') or t.get('id') or t.get('Test_case_id') or 'Unknown ID'
                    t_name = t.get('Test_Case_Name') or t.get('name') or t.get('Test_case_name') or 'Unknown Name'
                    t_desc = t.get('Description') or t.get('description') or 'No description provided'
                    
                    test_strings.append(f"  - [{t_id}] {t_name}: {t_desc}")
                    
                results.append(f"Scenario: {scenario}\n" + "\n".join(test_strings))
                
            return "\n\n".join(results)
    except Exception as e:
        return f"Database error: {str(e)}"