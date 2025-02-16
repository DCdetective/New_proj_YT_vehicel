import sys
import pandas as pd
import numpy as np
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.compose import ColumnTransformer

from src.logger import logging
from src.constants import TARGET_COLUMN,SCHEMA_FILE_PATH,CURRENT_YEAR
from src.entity.config_entity import DataTransformationConfig
from src.exception import MyException
from src.entity.artifact_entity import DataValidationArtifacts, DataTransformedArtifacts,DataIngestionArtifacts
from src.utils.main_utils import save_object,save_numpy_array_data, read_yaml_file


class DataTransformation:
    def __init__(self,data_ingestion_artifacts: DataIngestionArtifacts,
                 data_validation_artifacts: DataValidationArtifacts,
                 data_transformation_config: DataTransformationConfig):
        
        try:
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.data_validation_artifacts = data_validation_artifacts
            self.data_transformation_config = data_transformation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            
        except Exception as e:
            raise MyException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)
        
    def get_data_transformer_object(self) -> Pipeline:
        try:
            numeric_transformer = StandardScaler()
            min_max_scaler = MinMaxScaler()
            logging.info("Transformer Initialized: StandardScaler and MinmaxScaler")
            
            num_features = self._schema_config['num_features']
            mm_columns = self._schema_config['mm_columns']
            logging.info("cols loaded from schema")
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ("StandardScaler" , numeric_transformer,num_features),
                    ("MinMaxScaler" , min_max_scaler , mm_columns)
                ],
                remainder= 'passthrough'
            )
            final_pipeline = Pipeline(steps= [("Preprocessor",preprocessor)])
            logging.info("Final Pipeline Ready")
            logging.info("Exited get_data_Transformer obejct of DataTransformer")
            
            return final_pipeline
        
        except Exception as e:
            raise MyException(e, sys)
    
    def _map_gender_column(self,df):
        logging.info("Mapping 'Gender' column to binary values")
        df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1}).astype(int)
        return df
    
    def _create_dummy_columns(self,df):
        logging.info("Creating dummy varialnes for categorical features")
        df = pd.get_dummies(df,drop_first=True)
        return df
    
    def _rename_columns(self, df):
        """Rename specific columns and ensure integer types for dummy columns."""
        logging.info("Renaming specific columns and casting to int")
        df = df.rename(columns={
            "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
        })
        for col in ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]:
            if col in df.columns:
                df[col] = df[col].astype('int')
        return df

    def _drop_id_column(self, df):
        """Drop the 'id' column if it exists."""
        logging.info("Dropping 'id' column")
        drop_col = self._schema_config['drop_columns']
        if drop_col in df.columns:
            df = df.drop(drop_col, axis=1)
        return df

    def initiate_data_transformation(self) -> DataTransformedArtifacts:
        """
        Initiates the data transformation component for the pipeline.
        """
        try:
            logging.info("Data Transformation Started !!!")
            if not self.data_validation_artifacts.validation_status:
                raise Exception(self.data_validation_artifacts.message)

            # Load train and test data
            train_df = self.read_data(file_path=self.data_ingestion_artifacts.trained_file_path)
            test_df = self.read_data(file_path=self.data_ingestion_artifacts.test_file_path)
            logging.info("Train-Test data loaded")

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            logging.info("Input and Target cols defined for both train and test df.")

            # Apply custom transformations in specified sequence
            input_feature_train_df = self._map_gender_column(input_feature_train_df)
            input_feature_train_df = self._drop_id_column(input_feature_train_df)
            input_feature_train_df = self._create_dummy_columns(input_feature_train_df)
            input_feature_train_df = self._rename_columns(input_feature_train_df)

            input_feature_test_df = self._map_gender_column(input_feature_test_df)
            input_feature_test_df = self._drop_id_column(input_feature_test_df)
            input_feature_test_df = self._create_dummy_columns(input_feature_test_df)
            input_feature_test_df = self._rename_columns(input_feature_test_df)
            logging.info("Custom transformations applied to train and test data")

            logging.info("Starting data transformation")
            preprocessor = self.get_data_transformer_object()
            logging.info("Got the preprocessor object")

            logging.info("Initializing transformation for Training-data")
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            logging.info("Initializing transformation for Testing-data")
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)
            logging.info("Transformation done end to end to train-test df.")

            logging.info("Applying SMOTEENN for handling imbalanced dataset.")
            smt = SMOTEENN(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df
            )
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df
            )
            logging.info("SMOTEENN applied to train-test df.")

            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]
            logging.info("feature-target concatenation done for train-test df.")

            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            logging.info("Saving transformation object and transformed files.")

            logging.info("Data transformation completed successfully")
            return DataTransformedArtifacts(
                transformed_object_file=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file=self.data_transformation_config.transformed_test_file_path
            )
        except Exception as e:
            raise MyException(e, sys) from e