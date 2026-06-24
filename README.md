# 🕵️‍♂️ Intelligent Test Selector Agent

An AI-powered QA orchestration tool that intelligently maps developer code changes to specific business scenarios and test cases. By bridging the unstructured reasoning of Large Language Models (LLMs) with the deterministic relationships of a Neo4j Graph Database, this agent guarantees accurate, hallucination-free test coverage recommendations.

## 🌟 Features

* **Natural Language Extraction:** Developers can simply state what they changed in plain English (e.g., *"I updated the TokenValidator code"*).
* **Deterministic Graph Traversal:** Uses Neo4j to trace exact dependencies from Code Component $\rightarrow$ Business Scenario $\rightarrow$ Test Case.
* **Agentic Orchestration:** Built with LangGraph to strictly sequence the workflow (Extraction $\rightarrow$ Retrieval $\rightarrow$ Synthesis).
* **Interactive Web UI:** A sleek, conversational interface built with Streamlit.

## 🏗️ Architecture Stack

* **UI Layer:** Streamlit
* **Orchestration:** LangGraph (Python)
* **LLM Provider:** Google Gemini (2.5 Flash)
* **Knowledge Graph:** Neo4j (AuraDB Free)

---


https://github.com/user-attachments/assets/2bfd84c3-4546-46a9-82d3-69ca8c1623d1




## 📂 Project Structure

```text
test-selector-agent/
├── app.py                # Streamlit Web UI
├── main.py               # CLI entry point
├── graph.py              # LangGraph state and node logic
├── database.py           # Neo4j connection and Cypher queries
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (not tracked in git)

```

---

## 🚀 Getting Started

### 1. Prerequisites

* Python 3.8 or higher.
* A free [Neo4j AuraDB](https://neo4j.com/cloud/platform/aura-graph-database/) instance.
* A Google Gemini API Key (via [Google AI Studio](https://aistudio.google.com/)).

### 2. Installation

Clone this repository or create the project folder, then set up your environment:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 3. Environment Configuration

Create a `.env` file in the root directory and add your credentials:

```env
NEO4J_URI=neo4j+s://<YOUR_AURA_ID>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
GEMINI_API_KEY=your_gemini_api_key

```

### 4. Database Seeding

Before running the agent, you must populate your Neo4j database with the dependency graph. Open your Neo4j Workspace Query tab and execute the following Cypher script:

```cypher
MATCH (n) DETACH DELETE n;

CREATE (auth:Component {Component_Name: 'AuthService'})
CREATE (ui:Component {Component_Name: 'UserProfileUI'})
CREATE (validator:Component {Component_Name: 'TokenValidator'})
CREATE (email:Component {Component_Name: 'EmailDispatcher'})

CREATE (login:Scenario {Scenario_Name: 'User Login'})
CREATE (reset:Scenario {Scenario_Name: 'Password Reset'})
CREATE (session:Scenario {Scenario_Name: 'Session Mgmt'})

CREATE (tc101:TestCase {Test_Case_ID: 'TC-101', Test_Case_Name: 'Valid Credentials Login', Description: 'Verifies the happy path.'})
CREATE (tc102:TestCase {Test_Case_ID: 'TC-102', Test_Case_Name: 'Invalid Password Rejection', Description: 'Ensures the system denies access.'})
CREATE (tc103:TestCase {Test_Case_ID: 'TC-103', Test_Case_Name: 'Account Lockout', Description: 'Validates rate-limiting.'})
CREATE (tc201:TestCase {Test_Case_ID: 'TC-201', Test_Case_Name: 'Reset Link Generation', Description: 'Confirms valid recovery token.'})
CREATE (tc202:TestCase {Test_Case_ID: 'TC-202', Test_Case_Name: 'Expired Token Handling', Description: 'Verifies token expiration.'})
CREATE (tc301:TestCase {Test_Case_ID: 'TC-301', Test_Case_Name: 'Auto-logout', Description: 'Ensures abandoned sessions timeout.'})

CREATE (auth)-[:Participates_in]->(login)
CREATE (auth)-[:Participates_in]->(reset)
CREATE (ui)-[:Participates_in]->(login)
CREATE (validator)-[:Participates_in]->(reset)
CREATE (validator)-[:Participates_in]->(session)
CREATE (email)-[:Participates_in]->(reset)

CREATE (login)-[:Covered_by]->(tc101)
CREATE (login)-[:Covered_by]->(tc102)
CREATE (login)-[:Covered_by]->(tc103)
CREATE (reset)-[:Covered_by]->(tc201)
CREATE (reset)-[:Covered_by]->(tc202)
CREATE (session)-[:Covered_by]->(tc301);

```
<img width="880" height="447" alt="Screenshot 2026-06-25 021433" src="https://github.com/user-attachments/assets/5a319b97-0bba-4bb8-ab67-658ba64fa502" />

---

## 💻 Usage

**Run the Streamlit Web UI (Recommended):**

```bash
streamlit run app.py

```

This will open an interactive chat interface in your browser (default: `http://localhost:8501`).

**Run the CLI Version:**

```bash
python main.py

```

**Example Prompts to Try:**

* *"I just updated the TokenValidator code."*
* *"Made some UI changes to UserProfileUI."*
* *"Refactored the core database connection."* (Tests the agent's ability to handle unknown components gracefully).

---
