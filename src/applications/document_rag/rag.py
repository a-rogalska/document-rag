from langchain_core.messages import SystemMessage
from langchain_core.messages import trim_messages
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from llm import llm
from llm import vector_store
from prompts import rag_system_prompt

trimmer = trim_messages(strategy="last", max_tokens=2, token_counter=len)


@tool(response_format="content")
def retrieve(query: str) -> list:
    """Retrieve information related to a query."""
    retrieved_docs = vector_store.similarity_search(query)
    return retrieved_docs


def query_or_respond(state: MessagesState) -> dict:
    """Generate tool call for retrieval or respond."""
    llm_with_tools = llm.bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def generate(state: MessagesState) -> dict:
    """Generate answer."""
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]
    trimmed_messages = trimmer.invoke(conversation_messages)
    prompt = [SystemMessage(rag_system_prompt.format(docs_content=docs_content))] + trimmed_messages

    response = llm.invoke(prompt)
    return {"messages": [response]}


def init_graph():
    tools = ToolNode([retrieve])
    graph_builder = StateGraph(MessagesState)

    graph_builder.add_node(query_or_respond)
    graph_builder.add_node(tools)
    graph_builder.add_node(generate)

    graph_builder.set_entry_point("query_or_respond")
    graph_builder.add_conditional_edges(
        "query_or_respond",
        tools_condition,
        {END: END, "tools": "tools"},
    )
    graph_builder.add_edge("tools", "generate")
    graph_builder.add_edge("generate", END)

    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    return graph


graph = init_graph()
