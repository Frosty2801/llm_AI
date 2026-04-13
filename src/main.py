# Main module for the LangChain chat assistant application.
# Handles chat orchestration, tool execution, memory management, and special commands.

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from src.models import llm
from src.prompts import (
    get_chat_system_prompt,
    get_document_qa_system_prompt,
    get_explainer_system_prompt,
    get_memory_summarizer_system_prompt,
    get_programming_tutor_system_prompt,
)
from src.schemas import ConceptExplanation
from src.tools import (
    add_numbers,
    list_study_documents,
    multiply_numbers,
    obtain_current_date_and_time,
    read_project_file,
    retrieve_study_context,
)

# List of available tools for the LLM to use
tools = [
    obtain_current_date_and_time,
    add_numbers,
    multiply_numbers,
    read_project_file,
    list_study_documents,
    retrieve_study_context,
]

# Bind tools to the LLM for tool calling
llm_with_tools = llm.bind_tools(tools)
# Create structured LLM for concept explanations
structured_llm = llm.with_structured_output(
    ConceptExplanation,
    method="function_calling",
)
# Registry to map tool names to tool functions
tool_registry = {tool.name: tool for tool in tools}
# Load system prompts
chat_system_prompt = get_chat_system_prompt()
explainer_system_prompt = get_explainer_system_prompt()
memory_summarizer_system_prompt = get_memory_summarizer_system_prompt()
programming_tutor_system_prompt = get_programming_tutor_system_prompt()
document_qa_system_prompt = get_document_qa_system_prompt()

# Constants for memory management
RECENT_MESSAGE_WINDOW = 6  # Number of recent messages to keep
SUMMARY_TRIGGER_THRESHOLD = 10  # Threshold to trigger memory summarization


def build_runtime_messages(
    conversation_messages: list,
    memory_summary: str,
) -> list:
    # Build the message list for LLM invocation, including system prompt and memory summary
    runtime_messages = [chat_system_prompt]

    if memory_summary:
        runtime_messages.append(
            SystemMessage(
                content=f"Conversation summary so far:\n{memory_summary}"
            )
        )

    runtime_messages.extend(conversation_messages)
    return runtime_messages


def update_memory_summary(
    conversation_messages: list,
    memory_summary: str,
) -> tuple[str, list]:
    # Update memory summary if conversation is long, keeping only recent messages
    if len(conversation_messages) <= SUMMARY_TRIGGER_THRESHOLD:
        return memory_summary, conversation_messages

    messages_to_keep = conversation_messages[-RECENT_MESSAGE_WINDOW:]
    messages_to_summarize = conversation_messages[:-RECENT_MESSAGE_WINDOW]

    summary_request = HumanMessage(
        content=(
            f"Current memory summary:\n{memory_summary or 'No summary yet.'}\n\n"
            "Update the memory summary using these older conversation messages:\n\n"
            f"{messages_to_summarize}"
        )
    )

    updated_summary = llm.invoke(
        [memory_summarizer_system_prompt, summary_request]
    ).content

    return updated_summary, messages_to_keep


def process_tool_calls(
    conversation_messages: list,
    memory_summary: str,
) -> tuple[str, list]:
    # Process tool calls in the conversation, execute tools, and get final response
    runtime_messages = build_runtime_messages(conversation_messages, memory_summary)
    response = llm_with_tools.invoke(runtime_messages)

    if response.tool_calls:
        print(
            f"\n   [⚙️ The AI decided to pause and use the tool: "
            f"'{response.tool_calls[0]['name']}']"
        )

        conversation_messages.append(response)

        for tool_call in response.tool_calls:
            selected_tool = tool_registry.get(tool_call["name"])

            if selected_tool is None:
                tool_result = (
                    f"Tool '{tool_call['name']}' is not available in the registry."
                )
            else:
                tool_result = selected_tool.invoke(tool_call["args"])

            print(
                "   [✅ Sending the tool result back: "
                f"{tool_result}]\n"
            )

            tool_message = ToolMessage(
                tool_call_id=tool_call["id"],
                name=tool_call["name"],
                content=str(tool_result),
            )
            conversation_messages.append(tool_message)

        runtime_messages = build_runtime_messages(
            conversation_messages,
            memory_summary,
        )
        final_answer = llm_with_tools.invoke(runtime_messages)
        print("AI:", final_answer.content)
        conversation_messages.append(final_answer)
        return update_memory_summary(conversation_messages, memory_summary)

    print("AI:", response.content)
    conversation_messages.append(response)
    return update_memory_summary(conversation_messages, memory_summary)


def explain_topic_with_structure(topic: str) -> None:
    # Explain a topic using structured output with predefined schema
    structured_response = structured_llm.invoke(
        [
            explainer_system_prompt,
            HumanMessage(
                content=(
                    "Explain the following topic with a structured educational response: "
                    f"{topic}"
                )
            ),
        ]
    )

    print("AI Structured Response:")
    print(f"- Topic: {structured_response.topic}")
    print(f"- Difficulty level: {structured_response.difficulty_level}")
    print(f"- Explanation: {structured_response.explanation}")
    print(f"- Example: {structured_response.example}")
    print(f"- Recommended next step: {structured_response.recommended_next_step}")


def run_tutor_session(topic: str) -> None:
    # Run a tutoring session for a programming topic
    study_context = retrieve_study_context.invoke({"query": topic})
    tutor_response = llm.invoke(
        [
            programming_tutor_system_prompt,
            HumanMessage(
                content=(
                    f"Topic to teach: {topic}\n\n"
                    f"Relevant study context:\n{study_context}\n\n"
                    "Explain the topic, give one practical example, and finish with a small exercise."
                )
            ),
        ]
    )

    print("AI Tutor:")
    print(tutor_response.content)


def answer_with_study_documents(question: str) -> None:
    # Answer questions using retrieved study documents
    study_context = retrieve_study_context.invoke({"query": question})
    response = llm.invoke(
        [
            document_qa_system_prompt,
            HumanMessage(
                content=(
                    f"Question: {question}\n\n"
                    f"Retrieved study context:\n{study_context}"
                )
            ),
        ]
    )

    print("AI Study Answer:")
    print(response.content)


def start_chat() -> None:
    # Main chat loop handling user input and special commands
    conversation_messages = []
    memory_summary = ""

    print("Welcome to the chat. I am your software and LangChain assistant.")
    print("Write 'exit' or 'quit' to stop the execution.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Leaving chat...")
            break

        if user_input.lower().startswith("/explain "):
            topic = user_input[9:].strip()

            if not topic:
                print("AI: Please provide a topic after '/explain'.")
                continue

            explain_topic_with_structure(topic)
            continue

        if user_input.lower().startswith("/tutor "):
            topic = user_input[7:].strip()

            if not topic:
                print("AI: Please provide a topic after '/tutor'.")
                continue

            run_tutor_session(topic)
            continue

        if user_input.lower().startswith("/study "):
            question = user_input[7:].strip()

            if not question:
                print("AI: Please provide a question after '/study'.")
                continue

            answer_with_study_documents(question)
            continue

        if user_input.lower() == "/docs":
            available_docs = list_study_documents.invoke({})
            print("AI Study Documents:")
            print(available_docs)
            continue

        conversation_messages.append(HumanMessage(content=user_input))
        memory_summary, conversation_messages = process_tool_calls(
            conversation_messages,
            memory_summary,
        )


def main() -> None:
    # Entry point to start the chat application
    start_chat()


if __name__ == "__main__":
    main()

    print("Welcome to the chat. I am your software and LangChain assistant.")
    print("Write 'exit' or 'quit' to stop the execution.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Leaving chat...")
            break

        if user_input.lower().startswith("/explain "):
            topic = user_input[9:].strip()

            if not topic:
                print("AI: Please provide a topic after '/explain'.")
                continue

            explain_topic_with_structure(topic)
            continue

        if user_input.lower().startswith("/tutor "):
            topic = user_input[7:].strip()

            if not topic:
                print("AI: Please provide a topic after '/tutor'.")
                continue

            run_tutor_session(topic)
            continue

        if user_input.lower().startswith("/study "):
            question = user_input[7:].strip()

            if not question:
                print("AI: Please provide a question after '/study'.")
                continue

            answer_with_study_documents(question)
            continue

        if user_input.lower() == "/docs":
            available_docs = list_study_documents.invoke({})
            print("AI Study Documents:")
            print(available_docs)
            continue

        conversation_messages.append(HumanMessage(content=user_input))
        memory_summary, conversation_messages = process_tool_calls(
            conversation_messages,
            memory_summary,
        )


def main() -> None:
    start_chat()


if __name__ == "__main__":
    main()
