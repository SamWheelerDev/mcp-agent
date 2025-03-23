from mcp import ListToolsResult
import streamlit as st
import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM


def format_list_tools_result(list_tools_result: ListToolsResult):
    res = ""
    for tool in list_tools_result.tools:
        res += f"- **{tool.name}**: {tool.description}\n\n"
    return res


async def main():
    await app.initialize()

    meal_prep_agent = Agent(
        name="meal_prep_assistant",
        instruction="""You are a meal prep and cooking assistant with access to recipe databases 
        and nutrition information. Your job is to help users plan their meals for the week based on 
        their preferences, dietary restrictions, and ingredients they have available.
        
        Follow this conversation flow:
        1. Ask about dietary preferences and restrictions
        2. Inquire about ingredients they currently have
        3. Discuss their meal prep goals (number of meals, variety preferences)
        4. Suggest appropriate recipes and meal plans
        5. Provide cooking tips and substitutions when needed
        
        Be friendly, helpful, and provide detailed information about recipes including 
        ingredients, preparation steps, nutrition facts, and cooking times.""",
        server_names=["fetch", "filesystem"],  # Add recipe_db when available
    )
    await meal_prep_agent.initialize()
    llm = await meal_prep_agent.attach_llm(OpenAIAugmentedLLM)

    tools = await meal_prep_agent.list_tools()
    tools_str = format_list_tools_result(tools)

    st.title("🍲 Meal Prep Assistant")
    st.caption("🥗 Your personal meal planning and cooking companion")

    with st.expander("View Available Tools"):
        st.markdown(tools_str)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "Hi there! I'm your meal prep assistant. I can help you plan meals, suggest recipes, and provide cooking tips. Let's start by discussing your dietary preferences. Do you have any restrictions or preferences I should know about?",
            }
        ]

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Type your message here..."):
        st.session_state["messages"].append({"role": "user", "content": prompt})

        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            response = ""
            with st.spinner("Thinking..."):
                response = await llm.generate_str(
                    message=prompt, request_params=RequestParams(use_history=True)
                )
            st.markdown(response)

        st.session_state["messages"].append({"role": "assistant", "content": response})


if __name__ == "__main__":
    app = MCPApp(name="meal_prep_chatbot")

    asyncio.run(main())
