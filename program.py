import logging
from datetime import datetime

from browser_tools import setup_browser, download_data, extract_and_transform_data
from db_tools import Base
from db_tools import create_database_engine, create_session, insert_all_errands, create_tables
from utils import load_config_file, setup_logging


def main():
    start_time = datetime.now()
    setup_logging()
    configs = load_config_file()
    browser = setup_browser()
    soup = download_data(browser, configs)
    all_errands = extract_and_transform_data(soup)

    engine = create_database_engine(configs)
    create_tables(engine, Base)
    db_session = create_session(engine)

    insert_all_errands(db_session, all_errands)

    logging.info(f"Done after {datetime.now() - start_time}")


if __name__ == '__main__':
    main()
