import argparse
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from database.models import News

load_dotenv()

def init_conn():
    engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def list_posts(limit, offset, sort_by):
    session = init_conn()
    try:
        posts = session.query(News).order_by(
            func.cast(func.json_extract_path_text(News.meta, sort_by), Integer)
        ).limit(limit).offset(offset).all()
        for post in posts:
            print(post)
    except Exception as e:
        print(f'Error while fetching: {e}')
    finally:
        session.close()

def aggregate_posts(greater_than):
    session = init_conn()
    try:
        posts = session.query(News.date, func.count(News.id)).group_by(News.date).having(func.count(News.id) > greater_than).all()
        for date, count in posts:
            print(f'{date}: {count} Posts')
    except Exception as e:
        print(f'Error while fetching: {e}')
    finally:
        session.close()

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('--limit', type=int, default=10)
    list_parser.add_argument('--offset', type=int, default=0)
    list_parser.add_argument('--sort_by', type=str, default='points')

    aggr_parser = subparsers.add_parser('aggr')
    aggr_parser.add_argument('--greater_than', type=int, default=1)

    args = parser.parse_args()

    if args.command == 'list':
        list_posts(args.limit, args.offset, args.sort_by)
    elif args.command == 'aggr':
        aggregate_posts(args.greater_than)

if __name__ == '__main__':
    main()