import sys
from src.exception import MyException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher

from src.entity.config_entity import DataIngestionConfig , DataValidationConfig , DataTransformationConfig ,ModelTraninerConfig,ModelEvaluationConfig, ModelPusherConfig

from src.entity.artifact_entity import DataIngestionArtifacts, DataValidationArtifacts , DataTransformedArtifacts , ModelTrainerArtifacts , ModelEvaluationArtifact , ModelPusherArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_training_config = ModelTraninerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()
    def start_data_ingestion(self) -> DataIngestionArtifacts:
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config= self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifact
        except Exception as e:
            MyException(e , sys)
    
    def start_validation(self, data_ingestion_articats:DataIngestionArtifacts) -> DataValidationConfig:
        try:
            logging.info("Entering into Validation")
            data_validation = DataValidation(data_ingestion_artifacts= data_ingestion_articats , data_validation_config= self.data_validation_config)
            data_validation_artifacts = data_validation.initiate_data_validation()
            
            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")
            return data_validation_artifacts
        except Exception as e:
            MyException(e , sys)    
            
    def start_transformation(self, data_ingestion_artifacts: DataIngestionArtifacts , data_validation_artifacts:DataValidationArtifacts)-> DataTransformedArtifacts:
        try:
            data_transformation = DataTransformation(data_ingestion_artifacts= data_ingestion_artifacts , 
                                                     data_validation_artifacts= data_validation_artifacts,
                                                     data_transformation_config= self.data_transformation_config)
            data_transformation_artifacts = data_transformation.initiate_data_transformation()
            return data_transformation_artifacts
        except Exception as e:
            raise MyException(e, sys)
        
    def start_model_trainer(self, data_transformation_artifacts : DataTransformation)-> ModelTraninerConfig:
        try:
            model_trainer = ModelTrainer(data_transformation_artifacts= data_transformation_artifacts,
                                         model_trainer_config = self.model_training_config)
            
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            return model_trainer_artifacts        
        except Exception as e:
            raise MyException(e,sys)
    
    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifacts,
                               model_trainer_artifact: ModelTrainerArtifacts) -> ModelEvaluationArtifact:
        """S
        This method of TrainPipeline class is responsible for starting modle evaluation
        """
        try:
            model_evaluation = ModelEvaluation(model_eval_config=self.model_evaluation_config,
                                               data_ingestion_artifact=data_ingestion_artifact,
                                               model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e, sys)

    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        """
        This method of TrainPipeline class is responsible for starting model pushing
        """
        try:
            model_pusher = ModelPusher(model_evaluation_artifact=model_evaluation_artifact,
                                       model_pusher_config=self.model_pusher_config
                                       )
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e, sys)
        
    def run_pipeline(self , )-> None:
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            data_validation_artifacts = self.start_validation(data_ingestion_articats= data_ingestion_artifacts )
            data_transformation_artifacts = self.start_transformation(data_ingestion_artifacts= data_ingestion_artifacts , data_validation_artifacts= data_validation_artifacts )
            model_trainer_artifacts = self.start_model_trainer(data_transformation_artifacts=data_transformation_artifacts)
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifacts,
                                                                    model_trainer_artifact=model_trainer_artifacts)
            if not model_evaluation_artifact.is_model_accepted:
                logging.info(f"Model not accepted.")
                return None
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
        except Exception as e:
            raise MyException(e,sys)