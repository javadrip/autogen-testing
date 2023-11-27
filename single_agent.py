import os

import autogen

# NOTE: Not required if running models locally
# from dotenv import load_dotenv

# load_dotenv()

# chatgpt_key = os.getenv("CHATGPT_KEY")

config_list = [
    {
        # "model": "gpt-3.5-turbo-16k",
        # "api_type": "open_ai",
        "base_url": "http://localhost:1234/v1",
        "api_key": "NULL",  # NULL because running code locally
    }
]

llm_config = {
    "timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
}

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",  # Possible values: "ALWAYS", "TERMINATE", "NEVER".
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
    Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
)

assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="You are a creative copywriter who works in Ogilvy. Reply `TERMINATE` in the end when everything is done.",
    llm_config=llm_config,
)


task = """
Write a creative Kentucky Fried Chicken advertisement targeting vegans who are into the fit and healthy lifestyle.
"""

user_proxy.initiate_chat(assistant, message=task)
