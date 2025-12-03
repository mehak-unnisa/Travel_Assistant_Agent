# Core ADK Agent class used to define independent reasoning components.
from google.adk.agents import Agent

# AgentTool is used to wrap an entire agent as a callable tool inside another agent.
# This enables hierarchical / multi-agent orchestration.
from google.adk.tools.agent_tool import AgentTool

# Import custom tools for web-grounded search and OpenStreetMap place lookup.
from my_agent.tools import google_search_grounding, location_search_tool

# Gemini model wrapper provided by ADK for easy model selection.
from google.adk.models.google_llm import Gemini

# InMemoryRunner used when executing agents locally during development/testing.
from google.adk.runners import InMemoryRunner

# ADK's built-in Google Search tool (not directly used here but available).
from google.adk.tools import google_search

# Structured response types for future extension (classification, grounding, etc.)
from google.genai import types


# Shared model name for consistency across all sub-agents.
LLM = "gemini-2.5-flash"


# ---------------------------------------------------------------------------
# NEWS AGENT
# ---------------------------------------------------------------------------
# This agent specializes in retrieving travel-related news and events.
# It uses the google_search_grounding tool to perform real-time, web-grounded searches.
# It is intentionally restricted to 10 results for concise outputs.
news_agent = Agent(
    model=LLM,
    name="news_agent",
    description="Suggests key travel events and news; uses search for current info.",
    instruction="""
            You are responsible for providing a list of events and news recommendations based on the user's query. 
            Limit the choices to 10 results. You need to use the google_search_grounding agent tool to search the web for information.
        """,
    tools=[google_search_grounding]  # Web-grounded search tool (wrapped in a simple interface)
)


# ---------------------------------------------------------------------------
# PLACES AGENT
# ---------------------------------------------------------------------------
# This agent handles geographic place-based queries.
# It uses OpenStreetMap (OSM) via the location_search_tool to find POIs like hotels,
# landmarks, restaurants, and other coordinates-based results.
places_agent = Agent(
    model=LLM,
    name="places_agent",
    description="Suggests locations based on user preferences",
    instruction="""
            You are responsible for making suggestions on actual places based on the user's query. Limit the choices to 10 results.
            Each place must have a name, location, and address.
            You can use the places_tool to find the latitude and longitude of the place and address.
        """,
    tools=[location_search_tool]  # OSM-powered nearby place finder
)



# ---------------------------------------------------------------------------
# TRAVEL INSPIRATION AGENT (CORE AGENT)
# ---------------------------------------------------------------------------
# This is the main *intermediate* agent that the root agent delegates to.
# It orchestrates:
#   - destination inspiration
#   - activity suggestions
#   - event/news lookup
#   - place-based POI discovery
#
# DESIGN:
# - It does not handle raw data scraping. Instead, it delegates to specialized sub-agents.
# - The AgentTool wrapper allows this agent to CALL OTHER AGENTS as tools.
# - This supports modular, multi-agent reasoning with clean separation of concerns.
travel_inspiration_agent = Agent(
    model=LLM,
    name="travel_inspiration_agent",
    description="Inspires users with travel ideas. It may consult news and place agents",
    instruction="""
        You are travel inspiration agent who help users find their next big dream vacation destinations.
        Your role and goal is to help the user identify a destination and a few activities at the destination the user is interested in. 

        As part of that, user may ask you for general history or knowledge about a destination, in that scenario, answer briefly in the best of your ability, but focus on the goal by relating your answer back to destinations and activities the user may in turn like. Use tools directly when required without asking for feedback from the user. 

        - You will call the two tools `places_agent(inspiration query)` and `news_agent(inspiration query)` when appropriate:
        - Use `news_agent` to provide key events and news recommendations based on the user's query.
        - Use `places_agent` to provide a list of locations or nearby places to famous locations when user asks for it, for example "find hotels near eiffel tower", should return nearby hotels given some user preferences.
        """,

    # Wrapping other agents as tools enables dynamic delegation.
    # travel_inspiration_agent → (delegates to) → news_agent & places_agent
    tools=[AgentTool(agent=news_agent), AgentTool(agent=places_agent)]
)
