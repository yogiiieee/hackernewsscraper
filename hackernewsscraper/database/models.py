from sqlalchemy import create_engine, Integer, String, Date, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker, mapped_column, declarative_base

Base = declarative_base()

class News(Base):
    __tablename__ = 'hackernewspost'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    url: Mapped[str] = mapped_column(String(200), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    date: Mapped[str] = mapped_column(Date, nullable=True)
    meta: Mapped[dict] = mapped_column(JSON, nullable=False)

    def __repr__(self) -> str:
        points = self.meta.get('points', 'N/A')
        comments = self.meta.get('comments', 'N/A')
        return f'id: {self.id} | title: {self.title} | url: {self.url} | username: {self.username} | comments: {comments} | points: {points} | date: {self.date}'
