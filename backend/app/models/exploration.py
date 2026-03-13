from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Exploration(Base):
    __tablename__ = "explorations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    seed_topic = Column(String(512), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    nodes = relationship(
        "Node",
        back_populates="exploration",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
