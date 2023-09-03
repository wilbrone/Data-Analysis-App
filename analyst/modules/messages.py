from django.core.cache import cache

cache_timeout = 86400  # Cache data for 24 hours (24 * 60 * 60 seconds)
def save_chat_history(user_input, ai_response):
    # save the chat history in cache for future use.
    chat_history = []
    cached_chat_history = cache.get('chat_history', [])
    if cached_chat_history is not None:
        chat_history = cached_chat_history

        chat_history.append({'role': 'user', 'content': user_input})
        chat_history.append({'role': 'AI', 'content': ai_response})
        cache.set('chat_history', chat_history, cache_timeout)
    else:
        chat_history.append({'role': 'user', 'content': user_input})
        chat_history.append({'role': 'AI', 'content': ai_response})
        chat_history.append(ai_response)
        cache.set('chat_history', chat_history, cache_timeout)
    
    return


def get_chat_history():
    cached_chat_history = cache.get('chat_history', [])
    chat_history = []
    if cached_chat_history is not None:
        
        chat_history = cached_chat_history
    else:
        cached_chat_history = []

    return chat_history