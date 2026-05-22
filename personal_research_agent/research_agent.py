"""
Personal Research & Task Assistant AI Agent
============================================

A model-native AI agent that uses OpenAI's function calling to search the web
and answer questions with current information.

Author: Saeid Enayatpour
Date: 2026
"""

import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from ddgs import DDGS



# ===== CONFIGURATION =====

load_dotenv()

# Verify API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY not found. Please set it in .env file or environment."
    )

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model selection: "gpt-4-turbo-preview" or "gpt-3.5-turbo"
MODEL = "gpt-3.5-turbo"

# System prompt defining agent behavior
SYSTEM_PROMPT = """You are a helpful research assistant. Your goal is to answer user questions accurately using current information.

When you need current information or facts that may have changed recently, use the web_search tool.
After getting search results, synthesize the information into a clear, well-structured answer.
Always cite your sources when using web search results.

If you can answer a question from your training data alone (e.g., basic facts, definitions), you don't need to search.
"""


# ===== TOOL DEFINITIONS =====

def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo and return formatted results.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        Formatted string with search results including titles, URLs, and snippets
    """
    try:
        # Initialize DuckDuckGo search
        with DDGS() as ddgs:
            # Perform search and get results
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return "No results found for the query."
        
        # Format results for LLM consumption
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result['title']}\n"
                f"   URL: {result['href']}\n"
                f"   Summary: {result['body']}\n"
            )
        
        return "\n".join(formatted_results)
    
    except Exception as e:
        return f"Error performing search: {str(e)}"


# OpenAI function schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information on a topic. Use this when you need up-to-date information or facts that may have changed recently.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up on the web"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of search results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# Map function names to Python functions
available_functions = {
    "web_search": web_search
}


# ===== AGENT ORCHESTRATION LOOP =====

def run_agent(user_query: str, max_iterations: int = 5, verbose: bool = True) -> str:
    """
    Run the agent to answer a user query.
    
    Args:
        user_query: The user's question or request
        max_iterations: Maximum number of LLM-tool cycles (prevents infinite loops)
        verbose: Whether to print detailed logs
    
    Returns:
        Final answer from the agent
    """
    # Initialize conversation with system prompt and user query
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
    
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        if verbose:
            st.write(f"### Iteration {iteration}/{max_iterations}")
        
        try:
            # Call OpenAI API with function calling enabled
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto"  # Let the model decide if it needs tools
            )
            
            assistant_message = response.choices[0].message
            
            # Check if the model wants to call a function
            if assistant_message.tool_calls:
                # Add the assistant's message to conversation history
                messages.append(assistant_message)
                
                # Process each tool call (could be multiple in parallel)
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    if verbose:
                        st.info(f"🔧 Tool Call: {function_name}")
                        st.json(function_args)
                    
                    # Execute the function
                    if function_name in available_functions:
                        function_to_call = available_functions[function_name]
                        function_response = function_to_call(**function_args)
                        
                        if verbose:
                            st.success("Tool Response")
                            st.text(function_response[:1000])
                        
                        # Add function result to conversation
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": function_response
                        })
                    else:
                        st.warning(f"Warning: Unknown function {function_name}")
                
                # Continue the loop to get the final response
                continue
            
            # No tool calls - this is the final answer
            else:
                final_answer = assistant_message.content
                
                if verbose:
                    st.success(f"✅ Final Answer Generated in {iteration} iteration(s)")
                
                return final_answer
        
        except Exception as e:
            error_message = f"Error in agent loop: {str(e)}"
            st.error(error_message)
            return error_message
    
    # Max iterations reached
    return "Max iterations reached. The agent could not complete the task."


# ===== MAIN EXECUTION =====

def main():
    """Main execution function with example queries."""

    st.set_page_config(
        page_title="Personal Research & Task Assistant AI Agent",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖 Personal Research & Task Assistant AI Agent")
    st.markdown(
        """
        A model-native AI agent that uses OpenAI function calling and DuckDuckGo web search
        to answer questions with current information.
        """
    )

    st.divider()

    # Example queries
    example_queries = [
        "What are the latest developments in AI agents in 2024?",
        "Compare GPT-4 vs Claude 3 Opus for building agents",
        "Explain what a model-native agent is"
    ]

    selected_example = st.selectbox(
        "Choose an example query or write your own below:",
        [""] + example_queries
    )

    query = st.text_area(
        "Q: Enter your question:",
        value=selected_example,
        height=120
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        run_button = st.button(" Run Agent", use_container_width=True)

    with col2:
        verbose_mode = st.checkbox("Verbose Mode", value=True)

    if run_button:
        if not query.strip():
            st.warning("Please enter a valid question.")
        else:
            with st.spinner("Running AI Agent..."):
                answer = run_agent(query, verbose=verbose_mode)

            st.divider()

            st.subheader(" Final Answer")
            st.write(answer)


def interactive_mode():
    """Run the agent in interactive mode."""
    print("\n" + "="*60)
    print("Interactive Mode - Type 'quit' to exit")
    print("="*60 + "\n")
    
    while True:
        query = input("\n💭 Enter your question: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye! ")
            break
        
        if not query:
            print("Please enter a valid question.")
            continue
        
        print()
        answer = run_agent(query, verbose=True)
        
        print(f"\n{'='*60}")
        print("ANSWER")
        print(f"{'='*60}\n")
        print(answer)


if __name__ == "__main__":
    main()
    
    # Uncomment to enable interactive mode after the example
    interactive_mode()