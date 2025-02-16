from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    trained_file_path:str
    test_file_path:str
    
@dataclass
class DataValidationArtifacts:
    validation_status:bool
    message: str
    validation_report_file_path : str
    
@dataclass
class DataTransformedArtifacts:
    transformed_object_file:str
    transformed_train_file: str
    transformed_test_file: str
    
@dataclass
class ClassificationMetricArtifacts:
    f1_score: float
    precesion_score:float
    recall_score: float
    
@dataclass
class ModelTrainerArtifacts:
    trained_model_file_path: str
    metric_artifact:ClassificationMetricArtifacts
    
@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    changed_accuracy:float
    s3_model_path:str 
    trained_model_path:str

@dataclass
class ModelPusherArtifact:
    bucket_name:str
    s3_model_path:str