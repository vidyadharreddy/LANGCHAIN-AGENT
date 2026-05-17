import os
import certifi
from dotenv import load_dotenv,find_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.agents import tool
import requests
import streamlit as st

os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()
#load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

@tool
def whether_forecast(location)->str:
    """Get the weather forecast for a given location."""
    

    url=(f"https://api.weatherstack.com/current?"
         f"access_key={WEATHERSTACK_API_KEY}&query={location}")
    
    response=requests.get(url)
    data=response.json()

    if "current" not in data:
        return f"Could not retrieve weather data for {location}."

    return  f"The current weather in {location} is {data['current']['weather_descriptions'][0]} with a temperature of {data['current']['temperature']}°C."



search_tool = TavilySearchResults(max_results=2)
search_tool.invoke("What is the capital of France?")

prompt=hub.pull("hwchase17/react")
tools=[search_tool,whether_forecast]
llm=ChatGroq(model="llama-3.3-70b-versatile")

agent=create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor=AgentExecutor(agent=agent, tools=tools, verbose=True)
response=agent_executor.invoke({"input": "What is the capital of India? and its manjot IT hub locations with IT GBP"})

print(response["output"])


