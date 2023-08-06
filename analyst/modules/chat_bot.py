from django.conf import settings
from llama_index import OpenAIEmbedding, ServiceContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms import OpenAI
import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from langchain.vectorstores import DeepLake
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Necessary to use the latest OpenAI models that support function calling API
service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo-0613"))
documents = SimpleDirectoryReader('media').load_data()
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

# Test on some sample data
df = pd.DataFrame(
    {"city": ["Toronto", "Tokyo", "Berlin"], "population": [2930000, 13960000, 3645000]},
)

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

def process_user_query(question):
    print(question,'ttettttrQQWW')
    chat_response = None
    example_convo = {
        "User": "thank you",
        "AI": "You are also capable of general conversation. Analyse the question if it it is not related to the dataset given please say so",
    }
    try:
        # query_engine = index.as_query_engine(response_mode="tree_summarize")
        # response = query_engine.query(question)
        prompt_question = f"""
            You are an intelligent, powerful, compasionate, creative, polite and smart AI data science assistant, with the ability to do the most complex of data anaylsis when prompted by a user.
            You can also provide a summary of the data when asked for a summary and provide accurate python code for data science algarithms in the respose

            You are asked to answer the following question:
            ==================
            {question}
            ==================
            Scan the entire dataset.
        """

        query_engine = PandasQueryEngine(df=df, verbose=True, service_context=service_context)
        response = query_engine.query(prompt_question)
        print(response, 'response---------######********************>>>>>>>')
        formated_response = response.response

        payload = {
           "trial": formated_response
        }

        print(formated_response, 'formated_response---------######')

        question_prompt = f"""
            You are asked to answer the following question:
            ==================
            {question}
            ===================
            Given the Answer 
            ==================
            Answer: {formated_response}, 
            ===================
            Make your references to {df}, FORMAT Answer in conversational summary
            If you cannot provide a conversational summary, MENTION you got the Answer, and explain why it is not so accurate.
            You can also provide a summary of the data when asked for a summary and provide accurate python code for data science algarithms in the respose
            ==================
        """

        chat_engine = index.as_chat_engine(chat_mode="openai", verbose=True)
        chat_response = chat_engine.chat(question_prompt)
        
    

        # display(Markdown(f"<b>{response}</b>"))

        # chat_engine.chat_repl()
        print(chat_response, 'response---------######')
        return chat_response
    except Exception as e:
        print(e)



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
    # Answer a genaral question

    print("formated_response is None")

    question_prompt = f"""
        You are an intelligent, compasionate, powerful, creative, polite and smart AI data science assistant, with the ability to do the most complex of data anaylsis when prompted by a user.

        You are asked to answer the following question:
        ==================
        {question}
        ===================
    """

    chat_engine = index.as_chat_engine(chat_mode="openai", verbose=True)
    chat_response = chat_engine.chat(question_prompt)



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