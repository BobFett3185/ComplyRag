import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.workflow import Context
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader



from dotenv import load_dotenv
import os
load_dotenv() # Load the .env file
OPENAIKEY = os.getenv("GEM_API_KEY") # Access the key


documents = SimpleDirectoryReader('data').load_data()
index = VectorStoreIndex.from_documents(documents)
queryEngine = index.as_query_engine()


def multiply(a, b): # returns the product of a and b
    return a * b


async def searchDocuments(query):
    response = await queryEngine.aquery(query)
    return str(response)


# create simple agent 
agent = FunctionAgent(
    tools=[multiply, searchDocuments], # pass all the functions here which the llm can use
    llm=OpenAI(model="gpt-4o-mini"),
    system_prompt="You are a helpful assistant that can do a variety of tasks including multiplying numbers and searching documents to answer questions. You can also keep track of conversation context",
    api_key=OPENAIKEY
)

context = Context(agent)


async def main():
    # Run the agent

    '''
    response = await agent.run("What is 1234 * 4567?")
    print(str(response))

    reponse1 = await agent.run("MY name is keane and I love pickles", ctx = context)
    response2 = await agent.run ("What is my name and what do I love?", ctx = context) # the agent should remember the context of the previous message and be able to answer this question correctly

    print (str(response2))
    '''

    reponse = await agent.run("where did the author go to college? also what is 6 * 7??")
    print(str(reponse))

# Run the agent
if __name__ == "__main__":
    asyncio.run(main())