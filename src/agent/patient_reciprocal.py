from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from settings import AppSettings

AppSettings.loadenv()

# Make sure your environment variables are set:
# For Claude: ANTHROPIC_API_KEY
# For ChatGPT: OPENAI_API_KEY

MODELS = {"claude": "claude-sonnet-4-5-20250929", "gpt": "gpt-4"}

SELECTED_MODEL = "claude"

# Set up model
if SELECTED_MODEL == "claude":
    llm = ChatAnthropic(model=MODELS[SELECTED_MODEL])
else:
    llm = ChatOpenAI(model=MODELS[SELECTED_MODEL])


# Define conversation state
class UserState(TypedDict, total=False):
    age: str
    gender: str
    family_history_cancer: str
    specific_cancer_type: str


def ask_age(state: UserState) -> UserState:
    answer = input("Bot: How old are you?\nYou: ")
    state["age"] = answer.strip()
    response = llm.invoke(
        f"The user is {state['age']} years old. Respond briefly and encouragingly."
    )
    print("Bot:", response.content)
    return state


def ask_gender(state: UserState) -> UserState:
    answer = input("Bot: What is your gender? (male/female/other)\nYou: ")
    state["gender"] = answer.strip()
    response = llm.invoke(
        f"The user is {state['gender']}. Respond briefly and encouragingly."
    )
    print("Bot:", response.content)
    return state


def ask_family_history(state: UserState) -> UserState:
    answer = input("Bot: Do you have any family history of cancer? (yes/no)\nYou: ")
    state["family_history_cancer"] = answer.strip().lower()
    response = llm.invoke(
        f"Family history of cancer: {state['family_history_cancer']}. Respond briefly and supportively."
    )
    print("Bot:", response.content)
    return state


def follow_up_if_yes(state: UserState) -> UserState:
    answer = input("Bot: Which type(s) of cancer are in your family?\nYou: ")
    state["specific_cancer_type"] = answer.strip()
    response = llm.invoke(
        f"Specific cancer types in family: {state['specific_cancer_type']}. Respond with understanding and support."
    )
    print("Bot:", response.content)
    return state


def closing(state: UserState) -> UserState:
    summary = (
        f"Summary — Age: {state.get('age')}, Gender: {state.get('gender')}, "
        f"Family history of cancer: {state.get('family_history_cancer')}"
    )
    if state.get("specific_cancer_type"):
        summary += f", Specific types: {state.get('specific_cancer_type')}"
    response = llm.invoke(
        summary + ". Provide a supportive closing message about health awareness."
    )
    print("Bot:", response.content)
    return state


def should_follow_up(state: UserState) -> str:
    return (
        "follow_up_if_yes" if state.get("family_history_cancer") == "yes" else "closing"
    )


# Build the graph
graph = StateGraph(UserState)
graph.add_node("ask_age", ask_age)
graph.add_node("ask_gender", ask_gender)
graph.add_node("ask_family_history", ask_family_history)
graph.add_node("follow_up_if_yes", follow_up_if_yes)
graph.add_node("closing", closing)

# Define edges
graph.add_edge(START, "ask_age")
graph.add_edge("ask_age", "ask_gender")
graph.add_edge("ask_gender", "ask_family_history")
graph.add_conditional_edges("ask_family_history", should_follow_up)
graph.add_edge("follow_up_if_yes", "closing")
graph.add_edge("closing", END)

# Compile and run the graph
app = graph.compile()
initial_state: UserState = {}
app.invoke(initial_state)
