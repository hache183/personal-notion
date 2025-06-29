"""
Database models using SQLAlchemy 2.x
Defines the Page model for storing notes
"""

from datetime import datetime
from typing import Optional


# NUOVO:
from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base class for all database models"""
    pass


class Page(Base):
    """Page model for storing individual notes/pages"""
    
    __tablename__ = 'pages'
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Page content
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False, default='')
    
    # Timestamps
created_at: Mapped[datetime] = mapped_column(
    DateTime, nullable=False, default=func.now()
)
updated_at: Mapped[datetime] = mapped_column(
    DateTime, nullable=False, default=func.now(), onupdate=func.now()
)
    
    def __repr__(self) -> str:
        """String representation of Page object"""
        return f'<Page(id={self.id}, title="{self.title[:30]}...")>'
    
    def summary(self, max_length: int = 150) -> str:
        """Return a summary of the page content"""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length].rsplit(' ', 1)[0] + '...'