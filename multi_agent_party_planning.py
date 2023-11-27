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
    name="User_proxy",
    system_message="A human admin.",
    # code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
)

party_planner = autogen.AssistantAgent(
    name="Party planner",
    system_message="""You are a party planner.
    You will have to plan parties based on some specifications and present it to the Customer.
    If the Customer doesn't like it, you have to revise your plan.
    Your job is done when the Customer is satisfied.
    """,
    llm_config=llm_config,
)

customer = autogen.AssistantAgent(
    name="Customer",
    system_message="""You are a Customer.
    You like parties that are big, extravagant and have a lot of alcohol.
    A Party planner will present a plan to you.
    If you're unhappy with it, give feedback to the Party planner.
    If you're happy, let the Party planner know you're satisfied.
    Reply "TERMINATE" when you're satisfied.
    """,
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, party_planner, customer],
    messages=[],
    max_round=10,
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

task = "Plan a 3-day party for 100 people in the city of Singapore."

user_proxy.initiate_chat(manager, message=task)
