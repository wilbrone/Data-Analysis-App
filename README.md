# DataSense: Data Analysis Assistant
DataSense is an AI powered Data Analysis application showcasing the capabilities of large language model. This program, driven by GPT-4, chains together LLM "thoughts", to autonomously answer any question you ask. DataSense pushes the boundaries of what is possible with AI.

## 🚀 Features

- 🌐 Internet access for searches and information gathering
- 💾 Long-term and short-term memory management
- 🧠 GPT-4 and/or GPT-3 instances for text generation
- 🔗 Access to popular websites and platforms
- 🔌 LlamaIndex & Langchain for model training
- 📚 Python data analysis and modulation libraries

## Setting up
* Download latest version from [Github]() use default branch main
* Change to working directory, activate your virtual environment 
    - Run `python -m venv virtual` to create vitual environment
    - Run `source virtual/bin/activate` (For MacOs/Linux) OR `virtual\Scripts\activate` (For Windows) to activate the virtual environment
    - To exit the virtual environment, run `deactivate`.
* Install the required packages from `requirments.txt` from with in the virtual environment.
    run `pip install -r requirements.txt` to install from requirements.txt file.
    OR
    run `pip install <package-name>`
* Then run the server `python manage.py runserver`

NOTE: Incase you install additional package, always remember to update the requirements.txt file to help other developers/contributors install all required packages.
      To update the requirements file, Run `pip freeze > requirements.txt`. And `pip freeze` to check installed packages.

## Using DataSense
* You can send your message to the api **send_question**. Your question should have the following format:-
    ```
    {
        "userId":"ObjectID of a real user in the DB",
        "sessionId":"ObjectId of a session or just leave it empty", 
        "questionType":"text", 
        "question":"Can you visualize the growth of a $25,000 investment with an annual return of 7.8% over 20 years?"
    }
    ```