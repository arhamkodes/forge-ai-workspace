from sqlalchemy import select

from database.connection import SessionLocal
from database.models import Workspace


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