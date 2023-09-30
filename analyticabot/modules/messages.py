from django.core.cache import cache
from langchain import OpenAI
from langchain.memory import ConversationSummaryBufferMemory

from django.conf import settings


cache_timeout = 86400  # Cache data for 24 hours (24 * 60 * 60 seconds)
def save_chat_history(user_input, ai_response):
    # save the chat history in cache for future use.
    chat_history = []
    cached_chat_history = cache.get('chat_history', [])
    # if cached_chat_history is not None:
    #     chat_history = cached_chat_history

    #     chat_history.append({'role': 'user', 'content': user_input})
    #     chat_history.append({'role': 'AI', 'content': ai_response})
    #     cache.set('chat_history', chat_history, cache_timeout)
    # else:

    cached_chat_history.append({'human': user_input, 'AI': ai_response if ai_response is not None else '' })
    # cached_chat_history.append({'role': 'AI', 'content': ai_response})

    # print(cached_chat_history, 'cached_chat_history-----------yyyyy')
    cache.set('chat_history', cached_chat_history, cache_timeout)
    
    return


def get_chat_history(question):
    open_ai_llm = OpenAI(openai_api_key=settings.OPENAI_API_KEY)
    conversation_memory = ConversationSummaryBufferMemory(llm=open_ai_llm, memory_key='history', return_messages=True)

    cached_chat_history = cache.get('chat_history', [])

    print(cached_chat_history, 'cached_chat_history')
    if len(cached_chat_history)>0:
        
        conversation_memory.clear()

        user_messages = reversed(cached_chat_history)

        for message in user_messages:

            # print(message, '*******')                                                                                             
            conversation_memory.save_context({"input": message['human']}, {"output": message['AI']})                                    

    return {"conversation_memory": conversation_memory}

    # return chat_history