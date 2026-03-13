from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from .exploration import Base


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(512), nullable=False, index=True)
    summary = Column(String(4000), nullable=True)
    exploration_id = Column(
        Integer,
        ForeignKey("explorations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    exploration = relationship("Exploration", back_populates="nodes")
    outgoing_edges = relationship(
        "Edge",
        foreign_keys="Edge.parent_node_id",
        back_populates="parent_node",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    incoming_edges = relationship(
        "Edge",
        foreign_keys="Edge.child_node_id",
        back_populates="child_node",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
