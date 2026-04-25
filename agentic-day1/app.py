from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# 1. String-based invocation: each call is isolated — no shared context between calls.
resp1 = llm.invoke("We are building an AI system for processing medical insurance claims.")
print(resp1.content)

# "this system" is ambiguous here — model never saw resp1, so it guesses or hallucinates.
resp2 = llm.invoke("What are the main risks in this system?")
print(resp2.content)

# 2. Message-based invocation works because the full conversation is passed in one call.
#    The model sees both messages together, so context is preserved across turns.

# 3. Ignoring message history in production breaks:
#    - Multi-turn coherence: bot forgets prior user input
#    - Decision accuracy: fraud flags or key details from earlier are lost
#    - Workflow integrity: multi-step processes (collect → validate → decide) fall apart


messages = [
    SystemMessage(content="You are a senior AI architect reviewing production systems."),
    HumanMessage(content="We are building an AI system for processing medical insurance claims."),
    HumanMessage(content="What are the main risks in this system?")
]
resp3 = llm.invoke(messages)
print(resp3.content)

# Reflection:
# Q1: Why did string-based invocation fail?
#     Each call is stateless — resp2 has no memory of resp1, so "this system" is unresolved.
#
# Q2: Why does message-based invocation work?
#     All messages are sent together in one call, so the model sees the full context.
#
# Q3: What breaks in production if we ignore message history?
#     Multi-turn conversations lose coherence, prior decisions/flags are forgotten,
#     and multi-step workflows (collect → validate → decide) fall apart.

