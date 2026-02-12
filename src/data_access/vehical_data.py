import sys 
import pandas as pd
import numpy as np 
from typing import Optional

from src.configuration.mongodb_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException
from src.logger import logging

class VehicleData:

    """
    A class to export MongoDB records as a pandas DataFrame.
    """

    def __init__(self) -> None:

        """
        Initialize the MongoDB client connection.
        """

        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)
        
    def export_collection_as_dataframe(self, collection_name:str, database_name: Optional[str] = None) -> pd.DataFrame:

        """
        Exports an entire MongoDB collection as a pandas Dataframe. 

        collection_name:str
            The name of the MongoDB collection to export.
        database_name: Optional[str]
            Name of the database (optional). Default to DATABASE_NAME.

        Returns:
        --------
        pd.Dataframe:
            DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NAN.
        """

        try: 
            # Access specific collection from the default or specified database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            # Convert collection data to DataFrame and preprocess
            logging.info("Fetching the data from MongoDB")
            df = pd.DataFrame(list(collection.find()))
            # print(df.head())
            logging.info(f"data fetched with len: {len(df)}")

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
                # print(df.head())
            df.replace({"na":np.nan}, inplace=True)
            return df 
        
        except Exception as e:
            raise MyException(e,sys)
    