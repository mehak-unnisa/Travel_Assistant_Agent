# Travel Assistant Agent 🌍✈️
The **Travel Assistant Agent** is an intelligent, multi-functional AI designed to streamline the entire travel planning process. 

## 📌 Problem Statement
Planning a trip is time-consuming and overwhelming. Travelers often spend hours switching between blogs, travel sites, and social media just to figure out:

- *Where can I go within my budget?* 
- *What destinations match my interests?*  
- *What is safe or family-friendly?*  
- *What activities are possible during a specific season?*

This project solves the **travel decision-fatigue problem** by providing instant, personalized travel inspiration using an AI agent.

## 🤖 Why Agents?  
Agents are the right solution because they:

- **Reason autonomously** to break down travel queries.  
- **Call tools dynamically**, such as filtering destinations or retrieving travel data.  
- **Store preferences** using memory to personalize suggestions.  
- Behave like a **smart travel planner**, not a simple chatbot.

Agents make the experience adaptive, contextual, and highly efficient.

## 🏗️ What I Created – Solution Overview  
A multi-agent system powered by **Google ADK**, capable of:

- **Destination & Trip Ideas**: Generates personalized suggestions for destinations, themes, and detailed trip itineraries based on user input.
- **Real-Time Context**: Surfaces **relevant travel news, event information, and advisories** by querying the web, ensuring all plans are based on current data.
- **Hyperlocal Discovery (OpenStreetMap)**: Finds nearby points of interest, including **hotels, cafes, restaurants, and landmarks**, leveraging the power of **OpenStreetMap (OSM)** data, requiring no external paid mapping API -keys.
- **Geospatial Intelligence**: Accurately **geocodes** locations (converts names/addresses to coordinates) and contextualizes all location information for precise planning.
- **Session continuity**: Maintaining session continuity without a DB by using adk web

## 🧩 Architecture  

```text
root_agent (travel_planner_main)
└── travel_inspiration_agent
    ├── news_agent (uses google_search_grounding tool)
    └── places_agent (uses location_search_tool -> Overpass + Nominatim)
```
<img width="582" height="432" alt="Screenshot 2025-11-28 at 2 36 48 AM" src="https://github.com/user-attachments/assets/daf49f8c-d3f6-4d59-8368-43e78f3c3c78" />

## 🛠️ The Build – Tools & Technologies  

The agent is designed to be runnable locally and utilizes open-source data. The following are the tools and technologies used:
- **Agent Framework**: Google ADK
- **Language Model**: Gemini-powered LLM Agent
- **Sessions**: InMemorySession in adk web
- **Language**: Python 
- **Geodata & POIs**: OpenStreetMap (Nominatim + Overpass API)
- **Web Search**: Google ADK Search Tool Wrapper

### Additional Build Details  
- **OpenStreetMap**  
  Used as the primary source of high-quality, open POI data.  
  Powers hotel, cafe, landmark, and attraction discovery without requiring any API keys.
- **Web Search**  
  Enables web-grounded retrieval of real-time events, travel advisories, trending destinations, and news updates.

These two components make the agent *both grounded and up-to-date*, combining open geospatial data with timely web information.

## Prerequisites
- Python 3.11+
- macOS / Linux / (Windows via WSL) recommended
- A Google API key (for ADK models/tools)
  
## Setup Instructions  

### 1. Clone the repository  
```bash
git clone https://github.com/<your-repo>.git
cd <your-repo>
```
### 2. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Install requirements
```bash
pip install -r requirements.txt
```
### 4. Set environment variables
Create a .env file:
```env
GOOGLE_API_KEY=your_api_key_here
```
### 4. Set environment variables
Create a .env file:
```env
GOOGLE_API_KEY=your_api_key_here
```
### 5. Run the project
```bash
adk run my_agent
```
If you can to interact with the agent in adk web:
```bash
adk run 
```





  
