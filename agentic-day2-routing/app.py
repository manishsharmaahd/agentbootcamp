from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

load_dotenv()

MODEL = "gpt-4.1-nano"

llm = ChatOpenAI(model=MODEL)

class SupportState(TypedDict):
    messages: Annotated[list[BaseMessage],operator.add]
    should_escalate:bool
    issue_type:str
    user_tier:str # 'vip or 'standard'

def route_by_tier(state: SupportState) -> str:
	"""Route based on user tier."""
	if state.get("user_tier") == "vip":
		return "vip_path"
	return "standard_path"
def check_user_tier_node(state: SupportState):
    firstMessage = state['messages'][0].content.lower()
    if 'vip' in firstMessage or 'premium' in firstMessage:
        user_tier = 'vip'
    else:
        user_tier = 'standard'
    return {'user_tier': user_tier}

def vip_agent_node(state:SupportState):
    """Vip path : fast lane, no escaltions"""
    # You can call an LLM here if you want.
	# For the assignment it is fine to just set a friendly VIP response.
    return {"should_escalate":False}
    
def standard_agent_node(state:SupportState):
    """Vip path : fast lane, no escaltions"""
    # You can call an LLM here if you want.
	# For the assignment it is fine to just set a friendly VIP response.
    return {"should_escalate":True}


def build_graph():
	workflow = StateGraph(SupportState)
	workflow.add_node("check_tier", check_user_tier_node)
	workflow.add_node("vip_agent", vip_agent_node)
	workflow.add_node("standard_agent", standard_agent_node)
	workflow.set_entry_point("check_tier")
	workflow.add_conditional_edges(
		"check_tier",
		route_by_tier,
		{
			"vip_path": "vip_agent",
			"standard_path": "standard_agent",
		},
	)
	workflow.add_edge("vip_agent", END)
	workflow.add_edge("standard_agent", END)
	return workflow.compile()

def main() -> None:
    graph= build_graph()
    vip_result = graph.invoke({
		"messages": [HumanMessage(content="I'm a VIP customer, please check my order")],
		"should_escalate": False,
		"issue_type": "",
		"user_tier": "",
	})
    print("VIP result:", vip_result.get("user_tier"), vip_result.get("should_escalate"))

    standard_result = graph.invoke({
		"messages": [HumanMessage(content="Check my order status")],
		"should_escalate": False,
		"issue_type": "",
		"user_tier": "",
	})
    print("Standard result:", standard_result.get("user_tier"), standard_result.get("should_escalate"))


if __name__ == "__main__":
	main()
