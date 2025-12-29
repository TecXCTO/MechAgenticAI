
# In agent.py
#from .custom_functions import get_fx_rate  # Relative import
#from google.adk.agents.llm_agent import Agent


import asyncio
import logging
import os
import uuid

#from kaggle_secrets import UserSecretsClient

#from google.adk.agents import Agent
#from google.adk.agents import LlmAgent
#from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent,LlmAgent

from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import Agent
#from google.adk.apps.app import App, EventsCompactionConfig
#from google.adk.apps.app import App, ResumabilityConfig
from google.adk.apps.app import App, EventsCompactionConfig, ResumabilityConfig

from google.adk.code_executors import BuiltInCodeExecutor


from google.adk.models.google_llm import Gemini
from google.adk.models.llm_request import LlmRequest

from google.adk.memory import InMemoryMemoryService

from google.adk.plugins.base_plugin import BasePlugin
from google.adk.plugins.logging_plugin import (
    LoggingPlugin,
)  # <---- 1. Import the Plugin


#from google.adk.runners import InMemoryRunner
#from google.adk.runners import Runner
from google.adk.runners import InMemoryRunner, Runner


#from google.adk.sessions import InMemorySessionService
#from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import DatabaseSessionService, InMemorySessionService

#from google.adk.tools import google_search
#from google.adk.tools import AgentTool, FunctionTool, google_search
#from google.adk.tools import google_search, AgentTool, ToolContext
#from google.adk.tools import load_memory, preload_memory

from google.adk.tools import AgentTool, FunctionTool, google_search, load_memory, preload_memory, ToolContext 
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.google_search_tool import google_search

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.tool_context import ToolContext

from google.genai import types

from mcp import StdioServerParameters
#from typing import Any, Dict
#from typing import List
from typing import Any, Dict, List
from .agents.user_interaction import import_export as ie

print("✅ ADK components imported successfully.")

# Clean up any previous logs
for log_file in ["logger.log", "web.log", "tunnel.log"]:
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"🧹 Cleaned up {log_file}")

# Configure logging with DEBUG log level.
logging.basicConfig(
    filename="logger.log",
    level=logging.DEBUG,
    format="%(filename)s:%(lineno)s %(levelname)s:%(message)s",
)
print("✅ Logging configured")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)


root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='root_agent',
    description="""A helpful assistant cum co-worker, as servent responsible for user's all questions, orders, commands, instructions, restrictions.""",
    instruction = """Answer user questions to the best of your knowledge and do jobs given by user, while keep following all given user questions, order, command, instruction, restrictions. reply and response properly with complete details accordingly best your knoledge.""",
    tools=[ie],
    # ... other parameters ...
    #tools=[get_fx_rate],
    output_key="root_record",  # The result of this agent will be stored in the session state with this key.
)
print(f'Hi, I am your Mechanical Agent AI Assistant.')

print("MechAgentAI Assitant agent setup complete.")
runner = InMemoryRunner(agent=root_agent)

print("Runner created.")
prompt=""
async def main_task():
    while True:
        prompt=input("Hello, Welcome to Mechanical Agentic AI. Please start your work, by giving me commands.")
        response = await runner.run_debug(prompt)

if __name__ == "__main__":
    asyncio.run(main_task()) # Run the async function using the asyncio event loop

