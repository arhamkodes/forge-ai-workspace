from database.repository import (
    create_workspace,
    get_chat_messages,
    get_workspaces,
    save_chat_message,
)
import streamlit as st


from services.ai_router import generate_ai_response


st.set_page_config(
    page_title="Forge AI Workspace",
    page_icon="🤖",
    layout="wide",
)


# -----------------------------
# Session State
# -----------------------------

if "selected_workspace_id" not in st.session_state:
    st.session_state.selected_workspace_id = None


# -----------------------------
# Load Workspaces
# -----------------------------

workspaces = get_workspaces()


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.header("Workspace")

    if workspaces:
        workspace_options = {
            workspace.name: workspace
            for workspace in workspaces
        }

        selected_workspace_name = st.selectbox(
            "Select a workspace",
            options=list(workspace_options.keys()),
        )

        selected_workspace = workspace_options[selected_workspace_name]

        st.divider()

        st.write("**Workspace ID:**", selected_workspace.id)

        if selected_workspace.description:
            st.write("**Description:**")
            st.caption(selected_workspace.description)
        else:
            st.caption("No description provided.")

        st.divider()

        st.caption("AI Provider")
        st.selectbox(
            "Choose provider",
            options=["gemini"],
            index=0,
        )

    else:
        selected_workspace = None
        st.info("Create a workspace to get started.")


# -----------------------------
# Load Persistent Chat History
# -----------------------------

if selected_workspace:
    if (
        st.session_state.selected_workspace_id
        != selected_workspace.id
    ):
        st.session_state.selected_workspace_id = selected_workspace.id


# -----------------------------
# Header
# -----------------------------

st.title("🤖 Forge AI Workspace")

if selected_workspace:
    st.caption(f"Current workspace: {selected_workspace.name}")
else:
    st.caption("Create a workspace to begin.")


# -----------------------------
# Create Workspace
# -----------------------------

with st.expander("Create a new workspace"):
    with st.form("create_workspace_form"):
        workspace_name = st.text_input(
            "Workspace name",
            placeholder="Example: AI Web Development",
        )

        workspace_description = st.text_area(
            "Description",
            placeholder="What will you use this workspace for?",
        )

        submitted = st.form_submit_button("Create workspace")

        if submitted:
            if not workspace_name.strip():
                st.error("Workspace name is required.")
            else:
                create_workspace(
                    name=workspace_name.strip(),
                    description=workspace_description.strip() or None,
                )

                st.success("Workspace created successfully.")
                st.rerun()


st.divider()


# -----------------------------
# Chat History
# -----------------------------

if selected_workspace:
    saved_messages = get_chat_messages(selected_workspace.id)

    for message in saved_messages:
        with st.chat_message(message.role):
            st.markdown(message.content)


# -----------------------------
# Chat Input
# -----------------------------

if selected_workspace:
    user_prompt = st.chat_input(
        "Ask something about your project..."
    )

    if user_prompt:
        save_chat_message(
            workspace_id=selected_workspace.id,
            role="user",
            content=user_prompt,
        )

        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = generate_ai_response(
                        message=user_prompt,
                        provider="gemini",
                        system_instruction=(
                            "You are an AI assistant inside a project "
                            "workspace. Give clear, practical, and helpful "
                            "answers. Keep the user's project context in mind."
                        ),
                    )

                    save_chat_message(
                        workspace_id=selected_workspace.id,
                        role="assistant",
                        content=response,
                    )

                    st.markdown(response)

                except Exception as error:
                    st.error(f"AI request failed: {error}")

else:
    st.info("Create or select a workspace before starting a chat.")