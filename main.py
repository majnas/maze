import os
from dotenv import load_dotenv
import warnings
import requests  # For the exchange rate tool
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool  # Import the tool decorator
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults


warnings.filterwarnings("ignore", category=DeprecationWarning)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define the addition tool using the @tool decorator
@tool
def addition(input_str: str) -> int:
    """
    Adds two numbers. Input should be two space-separated numbers, e.g., "2 3".
    """
    try:
        a, b = map(int, input_str.split())
        return a + b
    except Exception as e:
        raise ValueError("Input must contain exactly two integers separated by a space.") from e


# Define the exchange rate tool using the @tool decorator
@tool
def get_exchange_rate(input_str: str) -> float:
    """
    Get the latest exchange rate between two currencies.
    Expects input to be two space-separated currency codes, e.g., "USD EUR".
    """
    try:
        base_currency, target_currency = input_str.split()
    except ValueError:
        raise ValueError("Input should contain exactly two space-separated currency codes, e.g., 'USD EUR'.")

    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base_currency.lower()}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rate = data.get(base_currency.lower(), {}).get(target_currency.lower(), None)
        if rate is None:
            raise Exception(f"Exchange rate not found for {base_currency} to {target_currency}")
        return rate
    else:
        raise Exception(f"Failed to fetch exchange rate: {response.status_code}")

wrapper = DuckDuckGoSearchAPIWrapper(max_results=10)
web_search = DuckDuckGoSearchResults(api_wrapper=wrapper)


# Initialize the Chat Model
chat_model = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)

# Initialize the agent with both tools (addition and exchange rate)
agent = initialize_agent(
    tools=[addition, get_exchange_rate],
    llm=chat_model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Example query using both tools
#response = agent.invoke("What is 5 + 7? And what's the exchange rate from USD to EUR?")
#print(response)



print("--------------------------")
from langchain import hub
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

# Get the prompt
oaif_prompt = hub.pull("hwchase17/openai-functions-agent")
print(oaif_prompt)

tools = [web_search, get_exchange_rate]

# Create the agent
oaif_agent = create_tool_calling_agent(chat_model, tools, oaif_prompt)

# Create the Agent Executor
# This is the runtime for an agent. This is what actually calls the agent, executes the actions it chooses, passes the action outputs back to the agent, and repeats. I
oaif_agent_executor = AgentExecutor(agent=oaif_agent, tools=tools, verbose=True)
query = "When was langgraph cloud released? and how much is a dollar worth in japan rn"
response = oaif_agent_executor.invoke({"input": query})
print("\n", response)


