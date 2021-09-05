import datetime
from typing import List, Dict

import sqlalchemy
from sqlalchemy import Column, DateTime, BigInteger, VARCHAR, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text, func

Base = declarative_base()


class Errand(Base):
    __tablename__ = "errands"
    id = Column(BigInteger, primary_key=True, nullable=False, unique=True)
    created_date = Column(Date, nullable=False)
    scraped_datetime = Column(DateTime, default=func.current_timestamp())
    rekyl_errand_id = Column(BigInteger, nullable=False)
    errand_status = Column(VARCHAR(length=50), nullable=False)
    reporter = Column(VARCHAR(length=50), default="N/A")
    apartment = Column(VARCHAR(length=50), default="N/A")
    errand_type = Column(VARCHAR(length=50), nullable=False)
    errand_details = Column(Text, default="N/A")


def create_database_engine(config_object, runs_local=False):
    if runs_local:
        db_url = config_object["linode_db"]["local_url"]
    else:
        db_url = config_object["linode_db"]["url"]

    return sqlalchemy.create_engine(db_url, echo=True)


def create_tables(db_engine, sql_alchemy_base_class):
    sql_alchemy_base_class.metadata.create_all(bind=db_engine)


def create_session(db_engine):
    return sessionmaker(bind=db_engine)


def describe_db_table(db_engine, table_name):
    with db_engine.connect() as connection:
        statement = text(f"DESCRIBE {table_name}")
        describe = connection.execute(statement)
        for row in describe:
            print(row)


def insert_all_errands(db_session, all_errands: List[Dict]):
    session = db_session()
    for errand_raw_data in all_errands:
        errand = Errand()

        errand.created_date = errand_raw_data.get("created_date")
        errand.rekyl_errand_id = errand_raw_data.get("rekyl_errand_id")
        errand.errand_status = errand_raw_data.get("errand_status")
        errand.reporter = errand_raw_data.get("reporter")
        errand.apartment = errand_raw_data.get("apartment")
        errand.errand_type = errand_raw_data.get("errand_type")
        errand.errand_details = errand_raw_data.get("errand_details")

        session.add(errand)

    session.commit()
    session.close()


def print_all_errands_statuses(db_session):
    session = db_session()

    errand_statuses = session.query(Errand.errand_status).distinct()

    for errand_status in errand_statuses:
        print(errand_status)

    session.close()


def print_all_errands_since_date(db_session, start_date):
    session = db_session()

    errands_since_date = session.query(Errand).filter(Errand.created_date >= start_date)

    session.close()

    for errand in errands_since_date:
        print(f"New errand: {errand} {type(errand)}")


if __name__ == "__main__":
    from utils import load_config_file, setup_logging

    setup_logging()
    configs = load_config_file()
    engine = create_database_engine(configs, runs_local=True)
    create_tables(engine, Base)
    db_session = create_session(engine)
    print_all_errands_statuses(db_session)
    date_two_days_ago = datetime.date.today() - datetime.timedelta(days=2)
    print_all_errands_since_date(db_session, date_two_days_ago)
