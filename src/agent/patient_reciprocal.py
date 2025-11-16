import uuid
from typing import TypedDict, List, Annotated

from IPython.display import Image, display

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END, add_messages

from agent.llm_chat_model_factory import LlmChatModelFactory


# Define conversation state
class PatientReciprocalState(TypedDict, total=False):
    # age: int
    # gender: str
    # family_history_cancer: str
    # specific_cancer_type: str
    messages: Annotated[list, add_messages]


class PatientReciprocalBot:
    SELECTED_MODEL_NAME = "claude"

    # class PromptInstructions(BaseModel):
    #     """Instructions on how to prompt the LLM."""
    #     objective: str
    #     variables: List[str]
    #     constraints: List[str]
    #     requirements: List[str]

    def __init__(self):
        self.llm = LlmChatModelFactory().create_model(self.SELECTED_MODEL_NAME)
        # self.llm = llm.bind_tools([PatientReciprocalState])
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
        self.app = self.build_graph()

    def get_messages_info(self, messages):
        return [SystemMessage(content=self.template)] + messages

    @staticmethod
    def get_state(state):
        messages = state["messages"]
        if isinstance(messages[-1], AIMessage) and messages[-1].tool_calls:
            return "add_tool_message"
        elif not isinstance(messages[-1], HumanMessage):
            return END
        return "get_info"

    def get_info_chain(self, state):
        messages = self.get_messages_info(state["messages"])
        response = self.llm.invoke(messages)
        return {"messages": [response]}

    def information_retrieved(self, state):
        print("information_retrieved:")
        print(state)

    def add_tool_message(self, state):
        return {
            "messages": [
                ToolMessage(
                    content="Prompt generated!",
                    tool_call_id=state["messages"][-1].tool_calls[0]["id"],
                )
            ]
        }

    def build_graph(self):
        # Build the graph
        memory = InMemorySaver()
        graph = StateGraph(PatientReciprocalState)
        graph.add_node("get_info", self.get_info_chain)
        graph.add_node("prompt", self.information_retrieved)
        graph.add_node("add_tool_message", self.add_tool_message)

        graph.add_edge(START, "get_info")
        graph.add_conditional_edges(
            "get_info",
            self.get_state,
            ["get_info", "add_tool_message", END]
        )
        compiled = graph.compile(checkpointer=memory)
        # display(Image(compiled.get_graph().draw_mermaid_png()))
        return compiled

    def run(self):
        cached_human_responses = ["Hi"]
        cached_response_index = 0
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        while True:
            try:
                user = input("User (q/Q to quit): ")
            except:
                user = cached_human_responses[cached_response_index]
                cached_response_index += 1
            print(f"User (q/Q to quit): {user}")
            if user in {"q", "Q"}:
                print("AI: Byebye")
                break
            output = None
            for output in self.app.stream(
            {"messages": [HumanMessage(content=user)]}, config=config, stream_mode="updates"
            ):
                last_message = next(iter(output.values()))["messages"][-1]
                last_message.pretty_print()

            if output and "prompt" in output:
                print("Done!")
        # self.app.invoke(self.state, config=config)
        # print("finished running")
        # return self.state


if __name__ == "__main__":
    bot = PatientReciprocalBot()
    state = bot.run()
    print(f"final state: ")
    print(state)
