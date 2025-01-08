from sqlalchemy import create_engine, MetaData
from models import News
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

News.metadata.create_all(engine)
session.close()