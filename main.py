import argparse
import subprocess
import yaml

from src import ApplicationProperties

def train_yolo(application_properties, dataset_location):
    image_size = str( application_properties.get_property_value("phase.training.image-size") )
    batch_size = str( application_properties.get_property_value("phase.training.batch-size") )
    num_epochs = str( application_properties.get_property_value("phase.training.num-epochs") )
    custom_model_location = application_properties.get_property_value("phase.training.custom-model-loc")
    custom_weights = application_properties.get_property_value("phase.training.weights")
    if not custom_weights:
        custom_weights = ""
    result_folder = application_properties.get_property_value("phase.training.output-dir")
    cache_images = application_properties.get_property_value("phase.training.cache-images")

    args = ["python", "yolov5/train.py", "--img", image_size, "--batch", batch_size, "--epochs", num_epochs, "--data", f"{dataset_location}/data.yaml", "--cfg", custom_model_location, "--weights", custom_weights, "--name", result_folder]
    if cache_images:
        args.append("--cache")

    print(f'Training arguments: {" ".join(map(str, args))}')

    subprocess.run(args)

    print("Yo completed")

if __name__ == '__main__':

    application_properties = ApplicationProperties("application.yml")
    application_properties.initializeProperties()

    dataset_location = application_properties.get_property_value("dataset.location")

    with open(dataset_location + "/data.yaml", 'r') as stream:
        num_classes = str(yaml.safe_load(stream)['nc'])

    train_yolo(application_properties, dataset_location)