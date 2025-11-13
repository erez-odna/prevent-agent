from langchain.agents import create_agent
from settings import AppSettings

AppSettings.loadenv()


# Make sure your environment variables are set:
# For Claude: ANTHROPIC_API_KEY
# For ChatGPT: OPENAI_API_KEY

MODELS = {"claude": "claude-sonnet-4-5-20250929", "gpt": "gpt-4"}

SELECTED_MODEL = "claude"

# Create a simple chatbot agent
agent = create_agent(
    model=MODELS[SELECTED_MODEL],
    tools=[],  # no external tools needed for this example
    system_prompt="You are a helpful assistant guiding a 3-step conversation.",
)

# Dictionary to store collected information
user_info = {}

# Conversation steps
steps = [
    {"role": "user", "content": "Hi, I'm here to answer a few questions."},  # greeting
]


def chat_step(user_input):
    """Send user input to the agent and return bot response text."""
    step_response = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]}
    )
    return step_response["messages"][-1].content


# Step 0: Greeting
bot_reply = chat_step("Greet the user and start the conversation.")
print("Bot:", bot_reply, "\n")

# Step 1: Ask age
user_info["age"] = input("Bot: How old are you?\nYou: ")
bot_reply = chat_step(f"The user is {user_info['age']} years old.")
print("Bot:", bot_reply, "\n")

# Step 2: Two-option question
print("\nStep 2: Two-option question")
response = agent.invoke(
    {"messages": steps + [{"role": "user", "content": "Do you prefer coffee or tea?"}]}
)
print("Bot:", response["messages"][-1].content)

# Step 3: Thank you message
print("\nStep 3: Thank you message")
response = agent.invoke(
    {"messages": steps + [{"role": "user", "content": "Thank you for participating!"}]}
)
print("Bot:", response["messages"][-1].content)
