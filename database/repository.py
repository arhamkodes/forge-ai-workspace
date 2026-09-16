from sqlalchemy import select

from database.connection import SessionLocal
from database.models import ChatMessage, Workspace


def create_workspace(
    name: str,
    description: str | None = None,
) -> Workspace:
    with SessionLocal() as session:
        workspace = Workspace(
            name=name,
            description=description,
        )

        session.add(workspace)
        session.commit()
        session.refresh(workspace)

        return workspace


def get_workspaces() -> list[Workspace]:
    with SessionLocal() as session:
        statement = select(Workspace).order_by(Workspace.created_at.desc())
        workspaces = session.scalars(statement).all()

        return list(workspaces)


def save_chat_message(
    workspace_id: int,
    role: str,
    content: str,
) -> ChatMessage:
    with SessionLocal() as session:
        message = ChatMessage(
            workspace_id=workspace_id,
            role=role,
            content=content,
        )

        session.add(message)
        session.commit()
        session.refresh(message)

        return message


def get_chat_messages(workspace_id: int) -> list[ChatMessage]:
    with SessionLocal() as session:
        statement = (
            select(ChatMessage)
            .where(ChatMessage.workspace_id == workspace_id)
            .order_by(ChatMessage.created_at.asc())
        )

        messages = session.scalars(statement).all()

        return list(messages)