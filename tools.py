# tools.py
class Sensor:
    def __init__(self, maze):
        self.maze = maze

    def read_distance(self, position, direction):
        # Calculate distance to the nearest obstacle in the specified direction
        x, y = position
        distance = 0
        while 0 <= x < len(self.maze.grid) and 0 <= y < len(self.maze.grid[0]):
            if self.maze.grid[x][y] == 1:
                break
            x += direction[0]
            y += direction[1]
            distance += 1
        return distance


# import requests  # For the exchange rate tool
# from langchain.tools import tool  # Import the tool decorator
# from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
# from langchain_community.tools import DuckDuckGoSearchResults

# # Define the addition tool using the @tool decorator
# @tool
# def addition(input_str: str) -> int:
#     """
#     Adds two numbers. Input should be two space-separated numbers, e.g., "2 3".
#     """
#     try:
#         a, b = map(int, input_str.split())
#         return a + b
#     except Exception as e:
#         raise ValueError("Input must contain exactly two integers separated by a space.") from e


# # Define the exchange rate tool using the @tool decorator
# @tool
# def get_exchange_rate(input_str: str) -> float:
#     """
#     Get the latest exchange rate between two currencies.
#     Expects input to be two space-separated currency codes, e.g., "USD EUR".
#     """
#     try:
#         base_currency, target_currency = input_str.split()
#     except ValueError:
#         raise ValueError("Input should contain exactly two space-separated currency codes, e.g., 'USD EUR'.")

#     url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base_currency.lower()}.json"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         rate = data.get(base_currency.lower(), {}).get(target_currency.lower(), None)
#         if rate is None:
#             raise Exception(f"Exchange rate not found for {base_currency} to {target_currency}")
#         return rate
#     else:
#         raise Exception(f"Failed to fetch exchange rate: {response.status_code}")

# wrapper = DuckDuckGoSearchAPIWrapper(max_results=10)
# web_search = DuckDuckGoSearchResults(api_wrapper=wrapper)