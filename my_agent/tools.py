# Import Google Search tool from ADK — allows LLM agents to perform grounded search queries.
from google.adk.tools.google_search_tool import google_search

# Base Agent class used to define autonomous reasoning units.
from google.adk.agents import Agent

# AgentTool allows wrapping an entire agent so it can be called as a tool by another agent.
from google.adk.tools.agent_tool import AgentTool

# Gemini wrapper enabling custom model configuration (e.g., retries, timeouts).
from google.adk.models.google_llm import Gemini

# ADK global search tools (duplicate import but harmless).
from google.adk.tools import google_search

# Types for retry configurations and structured responses.
from google.genai import types

# FunctionTool is used to expose Python functions as callable tools for agents.
from google.adk.tools import FunctionTool

# Geopy for geocoding physical addresses into coordinates.
from geopy.geocoders import Nominatim

# Requests used for Overpass API calls to OpenStreetMap.
import requests


# -------------------------------------------------------------------------
# RETRY CONFIGURATION FOR SEARCH AGENT
# -------------------------------------------------------------------------
# This configuration ensures reliability during Google Search calls by
# retrying when encountering API throttling or service errors.
retry_config = types.HttpRetryOptions(
    attempts=5,             # Maximum retry attempts
    exp_base=7,             # Exponential backoff multiplier
    initial_delay=1,        # Delay before first retry
    http_status_codes=[     # Retry only on transient server/limit errors
        429, 500, 503, 504
    ]
)

# Shared LLM setting for tools and agents.
LLM = "gemini-2.0-flash-001"


# -------------------------------------------------------------------------
# GOOGLE SEARCH WRAPPED AGENT
# -------------------------------------------------------------------------
# This agent is responsible for web-grounded search via Google's Search API.
# It returns BULLET-POINT results optimized for traveler usefulness.
# It is not the root agent — it is wrapped as a tool and called by other agents.
_search_agent = Agent(
    model=Gemini(
        model="gemini-2.5-flash-lite",  # Lightweight model for fast, tool-heavy workloads
        retry_options=retry_config       # Ensures resilient API calls
    ),
    name="google_search_wrapped_agent",
    description="An agent providing Google-search grounding capability",
    instruction="""
        Answer the user's question directly using google_search grounding tool; Provide a brief but concise response. 
        Rather than a detail response, provide the immediate actionable item for a tourist or traveler, in a single sentence.
        Do not ask the user to check or look up information for themselves, that's your role; do your best to be informative.
        IMPORTANT: 
        - Always return your response in bullet points
        - Specify what matters to the user
    """,
    tools=[google_search]  # Enables grounded internet search
)

# Wrap the above agent as a tool so other agents can call it.
google_search_grounding = AgentTool(agent=_search_agent)



# -------------------------------------------------------------------------
# FREE OPENSTREETMAP NEARBY PLACES TOOL
# -------------------------------------------------------------------------
# This function is the core of location_search_tool.
# It uses:
#   - Nominatim for free geocoding (no API key)
#   - Overpass API to query OSM for real POIs
# Goal:
#   Provide structured, free, API-keyless search for nearby places.
def find_nearby_places_open(query: str, location: str, radius: int = 3000, limit: int = 5) -> str:
    """
    Finds nearby places for any text query using ONLY free OpenStreetMap APIs (no API key needed).
    
    Args:
        query (str): What you’re looking for (e.g., "restaurant", "hospital", "gym", "bar").
        location (str): The city or area to search in.
        radius (int): Search radius in meters (default: 3000).
        limit (int): Number of results to show (default: 5).
    
    Returns:
        str: List of matching place names and addresses.
    """

    try:
        # Step 1: Geocode user-provided location into latitude & longitude.
        geolocator = Nominatim(user_agent="open_place_finder")
        loc = geolocator.geocode(location)
        if not loc:
            return f"Could not find location '{location}'."

        lat, lon = loc.latitude, loc.longitude

        # Step 2: Build Overpass API query.
        # The query matches:
        #  - Nodes with matching names
        #  - Amenity tags matching query (cafes, hotels, etc.)
        #  - Shop tags (stores, malls, etc.)
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json][timeout:25];
        (
          node["name"~"{query}", i](around:{radius},{lat},{lon});
          node["amenity"~"{query}", i](around:{radius},{lat},{lon});
          node["shop"~"{query}", i](around:{radius},{lat},{lon});
        );
        out body {limit};
        """

        # Step 3: Send the query to Overpass API
        response = requests.get(overpass_url, params={"data": overpass_query})
        if response.status_code != 200:
            return f"Overpass API error: {response.status_code}"

        data = response.json()
        elements = data.get("elements", [])
        if not elements:
            return f"No results found for '{query}' near {location}."

        # Step 4: Format a clean, user-friendly output
        output = [f"Top results for '{query}' near {location}:"]
        for el in elements[:limit]:
            name = el.get("tags", {}).get("name", "Unnamed place")
            street = el.get("tags", {}).get("addr:street", "")
            city = el.get("tags", {}).get("addr:city", "")
            full_addr = ", ".join(filter(None, [street, city]))
            output.append(f"- {name} | {full_addr if full_addr else 'Address not available'}")

        return "\n".join(output)

    except Exception as e:
        # Graceful fallback to avoid agent runtime errors.
        return f"Error searching for '{query}' near '{location}': {str(e)}"


# Expose find_nearby_places_open() as a tool usable by any ADK agent.
location_search_tool = FunctionTool(func=find_nearby_places_open)
