import streamlit as st

from database.repository import create_workspace, get_workspaces


st.set_page_config(
    page_title="Forge AI Workspace",
    page_icon="🤖",
    layout="wide",
)


st.title("🤖 Forge AI Workspace")
st.write("Your modular AI workspace platform.")


st.divider()

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

st.header("Your workspaces")

workspaces = get_workspaces()

if not workspaces:
    st.info("No workspaces yet. Create your first workspace above.")
else:
    for workspace in workspaces:
        with st.container(border=True):
            st.subheader(workspace.name)

            if workspace.description:
                st.write(workspace.description)
            else:
                st.caption("No description provided.")

            st.caption(
                f"Workspace ID: {workspace.id} | "
                f"Created: {workspace.created_at}"
            )