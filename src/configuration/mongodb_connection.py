import os 
import sys 
import pymongo
import certifi
from dotenv import load_dotenv
load_dotenv()

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY


# Load the certificate authority file to avoid timeout errors when connecting to mongodb

ca = certifi.where()

class MongoDBClient:

    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database.

    Attributes:
    -----------

    client : MongoClient
         A shared MongoClient instance for the class. 
    Database: Database
         The specific instance that MongoDBClient connects to.

    """

    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:

        """
        Initialize a connection to the MongoDB database. If no existing connection is found, it establishes a new one.
        """

        try:
            # check if a MongoDB client connection has already been establish; if not, create a new one.
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv("MONGODB_URL_KEY")
                if mongo_db_url is None:
                    raise Exception(f"Environment variable '{mongo_db_url}' is not set")
                
                # Establish a new MongoDB client connections
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful")

        except Exception as e:

            raise MyException(e, sys)
        