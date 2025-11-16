import re
from typing import TypedDict
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END

from agent.llm_chat_model_factory import LlmChatModelFactory


# Define conversation state
class PatientReciprocalState(TypedDict, total=False):
    age: int
    gender: str
    family_history_cancer: str
    specific_cancer_type: str


class PatientReciprocalBot:
    SELECTED_MODEL_NAME = "claude"

    def __init__(self):
        self.llm = LlmChatModelFactory().create_model(self.SELECTED_MODEL_NAME)
        self.llm.bind_tools()
        self.app = self.build_graph()
        self.state = PatientReciprocalState()
        self.template = template = """Your job is to get information from a user about their demographic and cancer history.
            You should get the following information from the user:
            
            - User age 
            - User birth gender
            - Whether the user has ever been diagnosed for cancer  
            - Whether the user has a family history of cancer, if yes then get the details of which cancer type each family member was diagnosed with               
            
            Be empathetic when the user reports self history of cancer of family history of cancer
            
            If you are not able to discern this info, ask them to clarify! Do not attempt to wildly guess.
            
            After you are able to discern all the information, call the relevant tool."""


    def ask_and_parse_age_node(self, state: dict):
        """
        If user_input is None, ask the question.
        Otherwise, validate the input.
        """
        print("Bot: Hi! I'm your cancer prevention agent.")
        answer = input("Bot: How old are you?\nYou: ")

        # parse result
        match = re.search(r"\d+", answer)
        if match:
            self.state["age"] = int(match.group())
            response = f"Got it. You’re {state['age']} years old."
            next_step = True
        else:
            response = "Sorry, I didn’t catch your age. Please enter a number."
            next_step = False
        return {"messages": [answer]}

    def ask_and_parse_gender_node(self, user_input: str = None):
        if user_input is None:
            return {"response": "What is your gender? (Male / Female / Other)"}

        gender = user_input.strip().capitalize()
        if gender in ["Male", "Female", "Other"]:
            self.state["gender"] = gender
            response = f"Thanks, I recorded your gender as {gender}."
            next_step = True
        else:
            response = "Please enter one of the following: Male, Female, or Other."
            next_step = False
        return {"response": response, "next_step": next_step, "gender": self.state.get("gender")}

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
        graph.add_node("age_node", self.ask_and_parse_age_node)
        graph.add_node("gender_node", self.ask_and_parse_gender_node)
        graph.add_node("ask_family_history", self.ask_family_history)
        graph.add_node("follow_up_if_yes", self.follow_up_if_yes)
        graph.add_node("closing", self.closing)

        graph.add_edge(START, "age_node")
        graph.add_conditional_edges(
            "age_node",
            lambda state: state.get("age") is None,
            ["age_node", "gender_node"]
        )
        graph.add_conditional_edges(
            "gender_node",
            lambda state: state.get("gender") is None,
            ["gender_node", "ask_family_history"]
        )

        graph.add_conditional_edges(
            "ask_family_history",
            self.should_follow_up,
            ["follow_up_if_yes", "closing"]
        )
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
