# main.py

import logging

from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_all
from scripts.config import setup_logger

logger = logging.getLogger(__name__)


def main():
    print("\n=== DATA PIPELINE ===\n")
    extract_data()
    transform_data()
    load_all()
    print("\n>>> PIPELINE COMPLETADO <<<\n")

if __name__ == '__main__':
    logger = setup_logger()
    main()
