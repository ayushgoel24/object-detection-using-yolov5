import argparse
import os
from pathlib import Path
import subprocess
import yaml

from src import ApplicationProperties

ROOT = Path(__file__).resolve().parents[0]

def train_yolo(application_properties, dataset_location):
    image_size = str( application_properties.get_property_value("phase.training.image-size") )
    batch_size = str( application_properties.get_property_value("phase.training.batch-size") )
    num_epochs = str( application_properties.get_property_value("phase.training.num-epochs") )
    datasetLocation = f"{dataset_location}/data.yaml"
    datasetLocation = os.path.join(ROOT, "yolov5", datasetLocation)
    custom_model_location = application_properties.get_property_value("phase.training.custom-model-loc")
    if not custom_model_location:
        custom_model_location = application_properties.get_property_value("phase.training.default-model")
    else:
        custom_model_location = os.path.join(ROOT, custom_model_location)
    custom_weights = application_properties.get_property_value("phase.training.weights")
    if not custom_weights:
        custom_weights = ""
    result_folder = application_properties.get_property_value("phase.training.output-dir")
    result_folder = os.path.join(ROOT, result_folder)

    cache_images = application_properties.get_property_value("phase.training.cache-images")

    args = ["python", "yolov5/train.py", "--img", image_size, "--batch", batch_size, "--epochs", num_epochs, "--data", datasetLocation, "--cfg", custom_model_location, "--weights", custom_weights, "--name", result_folder]
    if cache_images:
        args.append("--cache")

    subprocess.run(args)

def detect_yolo(application_properties):
    image_size = str( application_properties.get_property_value("phase.detection.image-size") )
    confidence_thres = str( application_properties.get_property_value("phase.detection.confidence-threshold") )
    trained_weights = application_properties.get_property_value("phase.detection.weights")
    test_images = application_properties.get_property_value("phase.detection.source")
    args = ["python", "yolov5/detect.py", "--img", image_size, "--conf", confidence_thres, "--weights", trained_weights, "--source", test_images]
    subprocess.run(args)

if __name__ == '__main__':

    application_properties = ApplicationProperties("application.yml")
    application_properties.initializeProperties()

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='train', help='train/detect')
    args = parser.parse_args()

    dataset_location = application_properties.get_property_value("dataset.location")

    if args.mode == 'train':
        train_yolo(application_properties, dataset_location)
    elif args.mode == 'detect':
        detect_yolo(application_properties)