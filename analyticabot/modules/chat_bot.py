

import os
import re
from codeinterpreterapi import CodeInterpreterSession, File
from django.conf import settings

from analyticabot.modules.messages import get_chat_history

full_file_path = os.path.join(settings.MEDIA_ROOT, '1YearCLEANED.csv')

def process_question(question):
    try:
        # Create a session and reuse it for multiple requests if needed
        with CodeInterpreterSession(model="gpt-3.5-turbo-16k") as session:
            # Define the user request
            user_request = question
            files = [
                # File(full_file_path)
                File.from_path(full_file_path)
            ]  # Add files if needed
            
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