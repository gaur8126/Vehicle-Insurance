import sys 
import pandas as pd 
from sklearn.pipeline import Pipeline


from src.exception import MyException
from src.logger import logging

class TargetValueMapping:
    def __init__(self):
        self.yes:int = 0
        self.no:int = 1
    def _asdict(self):
        return self.__dict__
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))

class MyModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        :param preprocessing_object: Input Object of preprocesser
        :param trained_model_object: Input Object of trained model 
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Function accepts preprocessed inputs (with all custom transformations already applied),
        applies scaling using preprocessing_object, and performs prediction on transformed features.
        """
        try:
            logging.info("Starting prediction process.")

            # Align input dataframe columns with the fitted preprocessor expectations
            try:
                preprocessor = None
                if isinstance(self.preprocessing_object, Pipeline):
                    preprocessor = self.preprocessing_object.named_steps.get("preprocessor")
                else:
                    preprocessor = self.preprocessing_object

                if preprocessor is not None and hasattr(preprocessor, "feature_names_in_"):
                    expected_cols = list(preprocessor.feature_names_in_)
                    missing_cols = [c for c in expected_cols if c not in dataframe.columns]
                    # add missing columns with default 0 values
                    for col in missing_cols:
                        dataframe[col] = 0
                    # reorder columns to match expected order
                    dataframe = dataframe[expected_cols]

            except Exception:
                # If alignment fails, fall back to original dataframe and let transform raise if needed
                logging.warning("Could not align input dataframe to preprocessor feature names; proceeding without alignment")

            # Step 1: Apply scaling transformations using the pre-trained preprocessing object
            transformed_feature = self.preprocessing_object.transform(dataframe)

            # Step 2: Perform prediction using the trained model
            logging.info("Using the trained model to get predictions")
            predictions = self.trained_model_object.predict(transformed_feature)

            return predictions

        except Exception as e:
            logging.error("Error occurred in predict method", exc_info=True)
            raise MyException(e, sys) from e


    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"