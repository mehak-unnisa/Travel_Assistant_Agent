# Travel Assistant Agent 🌍✈️

The **Travel Assistant Agent** is an intelligent, multi-functional AI designed to streamline the entire travel planning process. By combining up-to-the-minute web search capabilities with open-source geographical data, this agent moves beyond static itineraries to provide dynamic, relevant, and location-aware recommendations for any traveler.

## ✨ Features

This agent is built to be your digital concierge, offering the following core functionalities:
- **Destination & Trip Ideas**: Generates personalized suggestions for destinations, themes, and detailed trip itineraries based on user input.
- **Real-Time Context**: Surfaces **relevant travel news, event information, and advisories** by querying the web, ensuring all plans are based on current data.
- **Hyperlocal Discovery (OpenStreetMap)**: Finds nearby points of interest, including **hotels, cafes, restaurants, and landmarks**, leveraging the power of **OpenStreetMap (OSM)** data, requiring no external paid mapping API -keys.
- **Geospatial Intelligence**: Accurately **geocodes** locations (converts names/addresses to coordinates) and contextualizes all location information for precise planning.

## 🛠️ Technology Stack

The agent is designed to be runnable locally and utilizes open-source data:
- **Python**: Primary development language for the agent and logic.
- **OpenStreetMap**: Source for high-quality, free geographic and points-of-interest (POI) data.
- **LLM Integration**: (Assumed) Framework for natural language processing and conversational responses.
- **Web Search**: Powers the web-grounded search for real-time news and events.

## 🧠 Agent Architecture

The Travel Assistant Agent operates with a hierarchical structure:

* **root\_agent** (travel\_planner\_main)
    * **travel\_inspiration\_agent**
        * **news\_agent** (uses `Google Search_grounding` tool)
        * **places\_agent** (uses `location_search_tool` $\rightarrow$ Overpass + Nominatim)

### Agents:
- **Root Agent** - Entry point orchestration agent (delegates to inspiration)
- **Inspiration Agent** — suggests destinations & ideas
- **News Agent** — fetches grounded travel news & events
- **Places Agent** — uses OpenStreetMap Overpass API to find hotels, cafés, landmarks

### Tools:
- **google_search_grounding** - AgentTool wrapping search agent for concise bullet results
- **location_search_tool** - FunctionTool: find_nearby_places_open(query, location, radius, limit); 	Free OSM nearby place finder

## Prerequisites
- Python 3.11+
- macOS / Linux / (Windows via WSL) recommended
- A Google API key (for ADK models/tools) – store it in .env as GOOGLE_API_KEY=...



  
