import os
import re
from django.conf import settings
from llama_index import OpenAIEmbedding, ServiceContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms import OpenAI
import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from langchain.vectorstores import DeepLake
from langchain.text_splitter import RecursiveCharacterTextSplitter

from codeinterpreterapi import CodeInterpreterSession, File
import base64

from analyst.modules.messages import get_chat_history

# Necessary to use the latest OpenAI models that support function calling API
service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo-0613"))
documents = SimpleDirectoryReader('media').load_data()
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

# Test on some sample data
# df = pd.DataFrame(
#     {"city": ["Toronto", "Tokyo", "Berlin"], "population": [2930000, 13960000, 3645000]},
# )

# df = pd.DataFrame(
#    documents
# )

df = pd.read_csv("media/titanic_train.csv")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.create_documents(df)
embeddings = OpenAIEmbedding(model="text-embedding-ada-002")

# my_activeloop_org_id = settings.ACTIVELOOP_USERNAME
# my_activeloop_dataset_name = "data_sense_titanic_train"
# dataset_path = f"hub://{my_activeloop_org_id}/{my_activeloop_dataset_name}"
# db = DeepLake(dataset_path=dataset_path, embedding=embeddings)

# db.add_documents(docs)


def chat_bot_qeustion_predictions():
    examples_questions = [
        "What is the survival rate of the passengers?",
        "What is the average age of the passengers?",
        "How many male and female passengers are there?",
        "What is the distribution of passenger classes?",
        "What is the average fare paid by the passengers?",
        "How many siblings/spouses and parents/children are there for each passenger?",
        "What is the distribution of embarked ports?",
        "What is the most common cabin type?",
        "What is the distribution of passengers by name prefix (e.g. Mr., Mrs., Miss.)?",
        "What is the correlation between age and fare?"
    ]

    try:
        predict_prompt = f"""
            You are an intelligent, powerful, creative, polite and smart AI data science assistant, with the ability to do the most complex of data anaylsis when prompted by a user.
            You can also provide a summary of the data when asked for a summary and provide accurate python code for data science algarithms in the respose

            You are given the following data:
            ==================
            {df}
            ==================
            Provide a list of the top 10 most likely questions to be asked. Your response should be list format, .
        """

        chat_engine_II = index.as_chat_engine(chat_mode="openai", verbose=True)
        chat_response_II = chat_engine_II.chat(predict_prompt)

        print(chat_response_II, 'Response aprediction from the papers---------######')
        return chat_response_II
    except Exception as e:
        print(e)

def send_to_general(question):
    try:
        # Create a session and reuse it for multiple requests if needed
        with CodeInterpreterSession() as session:
            # Define the user request
            user_request = question
            files = []  # Add files if needed
            
            chat_history = get_chat_history()
            # Extend the chat history with the user's request
            chat_history.append({'role': 'user', 'content': f"""{user_request}\n Do not return any code in your response"""})

            my_string = f"""{chat_history}"""

            # Generate the response
            response = session.generate_response_sync(my_string, files=files)

            # Output to the user
            print("AI: ", response.content, '+****------>>', len(response.code_log))
            
            # Use regular expression to remove strings within triple backticks
            output_string = re.sub(r'```python(.*?)```', '', response.content, flags=re.DOTALL)
            
            result = {
                'response': output_string,
            }

            if response.files and response.code_log:
                print('------------------------_>>>>>>>>>>>>>>>>>>>>>>>__<<<<<>>', response.code_log[0], len(response.code_log))
                # result['file_names'] = [file.name for file in response.files]
                result['file'] = [file[1] for file in response.code_log]

            return result

    except Exception as e:  # Handle specific exceptions
        # Handle the exception, log, or return an error message
        print(f"Error: {e}")
        return {'error': str(e)}


def send_to_general_qw(question):
    # Answer a general question

    print("formated_response is None")

    # Check if the question is a Python code execution request
    if question.startswith("Calling function: python with args:"):
        # Extract the Python code from the question
        python_code = question.replace("Calling function: python with args:", "").strip()

        tools = {
        "python": {
            "execute": lambda code: exec(code),
        }
    }

        try:
            # # Execute the extracted Python code
            # exec(python_code)
            # response = "Python code executed successfully"

            # Use the "python" tool to execute the extracted Python code
            tool_name = "python"
            # tool = get_function_by_name(tools, tool_name)
            tool_output = tool["execute"](python_code)
            response = "Python code executed successfully"

        except Exception as e:
            response = f"Error while executing Python code: {str(e)}"
    else:
        # Normal question handling
        question_prompt = f"""
            You are an intelligent, compassionate, powerful, creative, witty, funny, polite, and smart AI data science assistant, with the ability to do the most complex data analysis when prompted by a user.

            You are asked to answer the following question:
            ==================
            {question}
            ===================
        """

        chat_engine = index.as_chat_engine(chat_mode="openai", verbose=True)
        chat_response = chat_engine.chat(question_prompt)
        response = chat_response['output']

    return response



def send_to_format_response(response, question):
    question_prompt = f"""
        You are asked to answer the following question:
        ==================
        {question}
        ===================
        Given the Answer 
        ==================
        Answer: {response}, 
        ===================
        Make your references to {df}, FORMAT Answer in conversational summary
        If you cannot provide a conversational summary, MENTION you got the Answer, and explain why it is not so accurate.
        You can also provide a summary of the data when asked for a summary and provide accurate python code for data science algarithms in the respose
        ==================
    """

    chat_engine = index.as_chat_engine(chat_mode="openai", verbose=True)
    chat_response = chat_engine.chat(question_prompt)