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

# Example from: https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat.ipynb

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
    human_input_mode="TERMINATE",
)
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
)
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config,
)
groupchat = autogen.GroupChat(agents=[user_proxy, coder, pm], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="Find a latest paper about gpt-4 on arxiv and find its potential applications in software.",
)
