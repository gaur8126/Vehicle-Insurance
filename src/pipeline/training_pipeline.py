import sys 
from src.exception import MyException
from src.logger import logging


from src.entity.config_entity import (DataIngestionConfig, 
                                      DataValidationConfig)

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataVlidation

from src.entity.artifact_entity import( DataIngestionArtifact, 
                                       DataValidationArtifact)



class TrainingPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()



    def start_data_ingestion(self) -> DataIngestionArtifact:

        """
        This method of traininf pipeline class is responsible for starting data ingestion components
        """

        try: 
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongodb")

            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info("Exited the start data ingestion methos of TrainPipeline class")

            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:

        try: 
            logging.info("Entered the start_data_validation method of traininf pipeline class")
            logging.info("Start data validation")

            data_validation = DataVlidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("data validation completed")
            logging.info("Exited the start data validation")

            return data_validation_artifact

        except Exception as e:
            raise MyException(e, sys) from e
        
    

    def run_pipeline(self,) -> None:

        """
        This methos of TrainingPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

        except Exception as e:
            raise MyException(e, sys) from e
