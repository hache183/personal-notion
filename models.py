"""
Database models using SQLAlchemy 1.4
Defines the Page model for storing notes
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Page(Base):
    """Page model for storing individual notes/pages"""
    
    __tablename__ = 'pages'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Page content
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False, default='')
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """String representation of Page object"""
        return f'<Page(id={self.id}, title="{self.title[:30]}...")>'
    
    def summary(self, max_length=150):
        """Return a summary of the page content"""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length].rsplit(' ', 1)[0] + '...'