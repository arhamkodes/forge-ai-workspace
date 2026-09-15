import streamlit as st

from database.repository import create_workspace, get_workspaces


st.set_page_config(
    page_title="Forge AI Workspace",
    page_icon="🤖",
    layout="wide",
)


# -----------------------------
# Page Header
# -----------------------------

st.title("🤖 Forge AI Workspace")
st.write("Your modular AI workspace platform.")


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

    else:
        selected_workspace = None
        st.info("Create a workspace to get started.")


# -----------------------------
# Create Workspace
# -----------------------------

st.header("Create a workspace")

with st.form("create_workspace_form"):
    workspace_name = st.text_input(
        "Workspace name",
        placeholder="Example: My AI Research Workspace",
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
# Selected Workspace
# -----------------------------

if selected_workspace:
    st.header(f"Workspace: {selected_workspace.name}")

    if selected_workspace.description:
        st.write(selected_workspace.description)
    else:
        st.caption("This workspace does not have a description yet.")

    st.info(
        "This is your selected workspace. "
        "Chat, documents, and AI tools will be connected here next."
    )

else:
    st.header("Welcome to Forge AI")
    st.write("Create your first workspace to begin.")