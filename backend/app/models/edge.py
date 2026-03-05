from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from .exploration import Base


class Edge(Base):
    __tablename__ = "edges"
    __table_args__ = (CheckConstraint("depth >= 0", name="ck_edges_depth_non_negative"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_node_id = Column(
        Integer,
        ForeignKey("nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    child_node_id = Column(
        Integer,
        ForeignKey("nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    depth = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    parent_node = relationship(
        "Node",
        foreign_keys=[parent_node_id],
        back_populates="outgoing_edges",
    )
    child_node = relationship(
        "Node",
        foreign_keys=[child_node_id],
        back_populates="incoming_edges",
    )
