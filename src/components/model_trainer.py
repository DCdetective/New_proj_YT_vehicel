import sys
from typing import Tuple

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score , precision_score , recall_score

from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import load_numpy_array_data,load_object,save_object
from src.entity.artifact_entity import DataTransformedArtifacts , ModelTrainerArtifacts , ClassificationMetricArtifacts
from src.entity.config_entity import ModelTraninerConfig
from src.entity.estimator import MyModel

class ModelTrainer:
    def __init__(self, data_transformation_artifacts: DataTransformedArtifacts ,
                 model_trainer_config: ModelTraninerConfig):
        try: 
            self.data_transformation_artifacts = data_transformation_artifacts
            self.model_tranier_config = model_trainer_config
        except Exception as e:
            raise MyException(e, sys) from e
    def get_model_object_and_reported(self, train: np.array , test: np.array) -> Tuple[object, object]:
        try:
            logging.info("Training RandomForestClassifier with specified Parameters")
            X_train,y_train,X_test,y_test = train[ : ,: -1], train[ : , -1], test[: , :-1], test[ : , -1]
            
            logging.info("Train_test_split is done")
            
            model = RandomForestClassifier(
                n_estimators= self.model_tranier_config._n_estimators,
                min_samples_split = self.model_tranier_config._min_sample_split,
                min_samples_leaf= self.model_tranier_config._min_sample_leaf,
                max_depth= self.model_tranier_config._max_dept,
                criterion= self.model_tranier_config._criterion,
                random_state=self.model_tranier_config._random_state
            )
            
            logging.info("Model training going on ....")
            model.fit(X_train , y_train)
            logging.info("Model Training done")
            
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_true= y_test , y_pred= y_pred)
            precision = precision_score(y_true= y_test , y_pred=y_pred)
            recall = recall_score(y_true= y_test , y_pred= y_pred)
            f1 = f1_score(y_true= y_test , y_pred= y_pred)
            
            metrics_artifact = ClassificationMetricArtifacts(f1_score= f1 , precesion_score = precision , recall_score= recall)
            
            return model , metrics_artifact
            
        except Exception as e:
            raise MyException(e, sys) from e
    
    def initiate_model_trainer(self) -> ModelTrainerArtifacts:
        logging.info("Entered into initiate_model_trainer method ModelTrainer class")
        
        try:
            train_arr = load_numpy_array_data(file_path= self.data_transformation_artifacts.transformed_train_file)
            test_arr = load_numpy_array_data(file_path = self.data_transformation_artifacts.transformed_test_file)
            logging.info("Model object and artifacts ")
            
            
            train_model, metric_artifact = self.get_model_object_and_reported(train= train_arr , test= test_arr )
            logging.info("Model object and artifact loaded")
            preprocessing_obj = load_object(file_path= self.data_transformation_artifacts.transformed_object_file)
            logging.info("Preprocessing object loaded")
            
            if accuracy_score(train_arr[: ,-1] , train_model.predict(train_arr[: , :-1])) < self.model_tranier_config.expected_accuracy:
                logging("No model found with score above the base score")
                
                raise Exception("no model found with score above the base score")
            
            logging.info("Saving new model as performance is better than previous one")
            my_model = MyModel( preprocessing_object = preprocessing_obj , trained_model_object= train_model)
            save_object(self.model_tranier_config.trained_model_file_path , my_model)
            logging.info("Saved final model object that includes both preprocessing and the trained model")
            
            model_trainer_artifact = ModelTrainerArtifacts(
                trained_model_file_path= self.model_tranier_config.trained_model_file_path,
                metric_artifact = metric_artifact,
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e, sys) from e