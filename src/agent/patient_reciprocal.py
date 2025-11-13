from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from agent.llm_chat_model_factory import LlmChatModelFactory


# Define conversation state
class PatientReciprocalState(TypedDict, total=False):
    age: str
    gender: str
    family_history_cancer: str
    specific_cancer_type: str


class PatientReciprocalBot:
    SELECTED_MODEL_NAME = "claude"

    def __init__(self):
        self.llm = LlmChatModelFactory().create_model(self.SELECTED_MODEL_NAME)
        self.app = self.build_graph()
        self.state = PatientReciprocalState()

    def ask_age(self, state: PatientReciprocalState):
        print("Bot: Hi! I'm your cancer prevention agent.")
        answer = input("Bot: How old are you?\nYou: ")
        self.state["age"] = answer.strip()
        response = self.llm.invoke(
            f"The user is {self.state['age']} years old. Respond briefly and encouragingly."
        )
        print("Bot:", response.content)
        return state

    def ask_gender(self, state: PatientReciprocalState):
        answer = input("Bot: What is your birth gender? (male/female)\nYou: ")
        self.state["gender"] = answer.strip()
        response = self.llm.invoke(
            f"The user is {self.state['gender']}. Respond briefly and encouragingly."
        )
        print("Bot:", response.content)
        return state

    def ask_family_history(self, state: PatientReciprocalState):
        answer = input("Bot: Do you have any family history of cancer? (yes/no)\nYou: ")
        self.state["family_history_cancer"] = answer.strip().lower()
        response = self.llm.invoke(
            f"Family history of cancer: {self.state['family_history_cancer']}. Respond briefly and supportively."
        )
        print("Bot:", response.content)
        return state

    def follow_up_if_yes(self, state: PatientReciprocalState):
        answer = input("Bot: Which type(s) of cancer are in your family?\nYou: ")
        self.state["specific_cancer_type"] = answer.strip()
        response = self.llm.invoke(
            f"Specific cancer types in family: {self.state['specific_cancer_type']}. Respond with understanding and support."
        )
        print("Bot:", response.content)
        return state

    def closing(self, state: PatientReciprocalState):
        summary = (
            f"Summary — Age: {state.get('age')}, Gender: {state.get('gender')}, "
            f"Family history of cancer: {state.get('family_history_cancer')}"
        )
        if state.get("specific_cancer_type"):
            summary += f", Specific types: {state.get('specific_cancer_type')}"
        response = self.llm.invoke(
            summary + ". Provide a supportive closing message about health awareness."
        )
        print("Bot:", response.content)
        return state

    def should_follow_up(self, state: PatientReciprocalState):
        return (
            "follow_up_if_yes"
            if state.get("family_history_cancer") == "yes"
            else "closing"
        )

    def build_graph(self):
        # Build the graph
        graph = StateGraph(PatientReciprocalState)
        graph.add_node("ask_age", self.ask_age)
        graph.add_node("ask_gender", self.ask_gender)
        graph.add_node("ask_family_history", self.ask_family_history)
        graph.add_node("follow_up_if_yes", self.follow_up_if_yes)
        graph.add_node("closing", self.closing)

        # Define edges
        graph.add_edge(START, "ask_age")
        graph.add_edge("ask_age", "ask_gender")
        graph.add_edge("ask_gender", "ask_family_history")
        graph.add_conditional_edges("ask_family_history", self.should_follow_up)
        graph.add_edge("follow_up_if_yes", "closing")
        graph.add_edge("closing", END)

        # Compile and run the graph
        return graph.compile()

    def run(self):
        self.app.invoke(self.state)
        print("Bot: Thank you for your responses. Goodbye!")
        return self.state


if __name__ == "__main__":
    bot = PatientReciprocalBot()
    state = bot.run()
    print(f"final state: ")
    print(state)
