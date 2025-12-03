# Import the base LLM Agent class from Google ADK.
# This provides planning, tool orchestration, and message handling.
from google.adk.agents.llm_agent import Agent

# Import the travel_inspiration_agent, which encapsulates the core multi-agent logic.
# This sub-agent handles destination generation, place lookup, and news retrieval.
from my_agent.supporting_agents import travel_inspiration_agent

# Import types for structured generation (not directly used here, but required by ADK patterns).
from google.genai import types


# Root agent definition.
# This is the primary entry point of the system and acts as the coordinator for all travel tasks.
root_agent = Agent(
    model="gemini-2.5-flash",  # Fast, reasoning-capable model suitable for planning and tool calling.
    name="travel_planner_main",  # Unique ID for tracking the agent within ADK’s execution graph.

    # High-level description: defines the agent's purpose and global persona.
    description=(
        "A helpful travel planning assistant that helps users plan their trips "
        "by providing information and suggestions based on their preferences."
    ),

    # System instructions that govern behavior and allowed capabilities.
    # These constraints ensure correct delegation and prevent misuse of tools.
    instruction="""
            - You are an exclusive travel concierge agent
            - You help users to discover their dream holiday destination and plan their vacation.
            - Use the inspiration_agent to get the best destination, news, places nearby e.g hotels, cafes, etc near attractions and points of interest for the user.
            - You cannot use any tool directly. 
            """,

    # Registering sub-agents.
    # This enables hierarchical reasoning: the root agent delegates specific tasks to the
    # travel_inspiration_agent instead of doing everything itself.
    #
    # The travel_inspiration_agent further delegates internally to:
    #   - news_agent (web-grounded travel news)
    #   - places_agent (OpenStreetMap POI search)
    # This creates a clean modular agent architecture.
    sub_agents=[travel_inspiration_agent],
)
