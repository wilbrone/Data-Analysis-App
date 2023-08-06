from llama_index import ServiceContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms import OpenAI

# Necessary to use the latest OpenAI models that support function calling API
service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo-0613"))
documents = SimpleDirectoryReader('media').load_data()
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

def process_user_query(question):
    print(question,'ttettttrQQWW')
    try:
        # query_engine = index.as_query_engine(response_mode="tree_summarize")
        # response = query_engine.query(question)

        chat_engine = index.as_chat_engine(chat_mode="openai", verbose=True)
        response = chat_engine.chat(question)

        # chat_engine.chat_repl()
        print(response, 'response---------######', )
        return response
    except Exception as e:
        print(e)