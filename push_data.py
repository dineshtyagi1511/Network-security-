import os
import sys
import json

from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

import certifi
ca = certifi.where()

import pandas as pd
from pymongo import MongoClient

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logger


class NetworkDataExtract:

    def __init__(self):
        try:
            logger.info("Initializing NetworkDataExtract class.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            logger.info(f"Reading CSV file from: {file_path}")

            data = pd.read_csv(file_path)
            logger.info(f"CSV loaded successfully. Shape: {data.shape}")

            data.reset_index(drop=True, inplace=True)

            records = list(json.loads(data.T.to_json()).values())

            logger.info(f"Successfully converted CSV to JSON. Total records: {len(records)}")

            return records

        except Exception as e:
            logger.exception("Error occurred while converting CSV to JSON.")
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            logger.info("Connecting to MongoDB Atlas...")

            self.mongo_client = MongoClient(
                MONGODB_URI,
                tls=True,
                tlsCAFile=ca
            )

            logger.info("Pinging MongoDB server...")

            self.mongo_client.admin.command("ping")

            logger.info("MongoDB connection established successfully.")

            self.database = self.mongo_client[database]
            self.collection = self.database[collection]

            logger.info(
                f"Inserting {len(records)} records into "
                f"Database='{database}', Collection='{collection}'"
            )

            self.collection.insert_many(records)

            logger.info("Data inserted successfully.")

            return len(records)

        except Exception as e:
            logger.exception("Failed to insert data into MongoDB.")
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":

    FILE_PATH = r"Network_Data\phisingData.csv"
    DATABASE = "DINESHTYAGI"
    COLLECTION = "NetworkData"

    try:
        logger.info("========== Data Ingestion Started ==========")

        network_obj = NetworkDataExtract()

        records = network_obj.csv_to_json_converter(FILE_PATH)

        inserted = network_obj.insert_data_mongodb(
            records,
            DATABASE,
            COLLECTION
        )

        logger.info(f"Successfully inserted {inserted} records.")
        print(f"Inserted {inserted} records.")

        logger.info("========== Data Ingestion Completed ==========")

    except Exception as e:
        logger.exception("Pipeline execution failed.")
        raise NetworkSecurityException(e, sys)