

import os
import re
from codeinterpreterapi import CodeInterpreterSession, File
from django.conf import settings

from analyticabot.modules.messages import get_chat_history

full_file_path = os.path.join(settings.MEDIA_ROOT, 'online_retail_II.xlsx')

def process_question(question):
    print(question, '------------------------')
    try:
        # result = None
        # Create a session and reuse it for multiple requests if needed
        with CodeInterpreterSession(model="gpt-3.5-turbo-16k") as session:
            # Define the user request
            user_request = question
            files = [
                # File(full_file_path)
                File.from_path(full_file_path)
            ]  # Add files if needed
            
            cached_chat_history = get_chat_history()
            chat_history = [
                {
                    'role': 'AI',
                    'content': chat['content']['response']
                } if chat['role'] == 'AI' else chat
                for chat in cached_chat_history
            ]

            # chat_history = chat.get('chat_history')
            # Extend the chat history with the user's request
            chat_history.append({
                'role': 'user',
                'content': f"""{user_request}
                NOTE: Be Professional, Precise, and Informative. Perform thorough and thoughtful analyses to assist with decision-making. Handle missing values and clean the dataset when possible. Avoid including any code in your final response to me.
                In case of errors in the dataset, please clean it and continue. If it's impossible, inform me and provide suggestions on resolving the issue.
                Always anticipate my needs and act accordingly.
                If you encounter an openai.error.InvalidRequestError, find a smart way to truncate messages by keeping the latest messages to reduce the message's token count.
                """
            })
            # sent_q = f"""{user_request}\n NOTE: Do not return any code in your response. If there is an error in the dataset please clean it and continue. If it is impossible let me know about it and give me suggestions on how you can help solve the error. Always predict what I want next and act on it"""
            my_string = f"""{chat_history[-4:]}"""
            print(my_string, '-----<---<--<-<-<-')
            
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
                print('------------------------_>>>>>>>>>>>>>>>>>>>>>>>__<<<<<>>', response.code_log[0], len(response.code_log), len(response.files))
                # result['file_names'] = [file.name for file in response.files]
                result['file'] = [file[1] for file in response.code_log]
                for file in response.files:
                    file.show_image()

            return result

    except Exception as e:  # Handle specific exceptions
        # Handle the exception, log, or return an error message
        print(f"Error: {e}")
        return {'error': str(e)}