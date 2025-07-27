#!/usr/bin/env python3

# How To manually submit into a ray cluster:
# cd into homeworks/project/job
# ray job submit --address=http://localhost:8265 --working-dir . -- python lenet_mnist_train.py --data-dir=/mnist --minio-endpoint=http://host.docker.internal:9000 --minio-access-key=ROOTUSER --minio-secret-key=CHANGEME123 --minio-bucket-name=mnist --minio-object-name=train-images-idx3-ubyte.gz

import os
import sys
import logging
import argparse
import boto3
from botocore.client import Config
from typing import Dict, Any

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import transforms, datasets

from ray.train.torch import TorchTrainer
from ray.air.config import ScalingConfig
from ray.air import session

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LeNet(nn.Module):
    """LeNet-5 model for MNIST classification"""

    def __init__(self, num_classes=10):
        super(LeNet, self).__init__()
        # Convolutional layers
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)

        # Max pooling layer
        self.pool = nn.MaxPool2d(2, 2)

        # Fully connected layers
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)

    def forward(self, x):
        # First convolutional layer + pooling
        x = self.pool(F.relu(self.conv1(x)))

        # Second convolutional layer + pooling
        x = self.pool(F.relu(self.conv2(x)))

        # Flatten for fully connected layers
        x = x.view(-1, 16 * 4 * 4)

        # Fully connected layers
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        return x


def download_and_extract_from_minio(endpoint_url, access_key, secret_key, bucket_name, object_name, local_dir):
    """Download and extract a specific file from a ZIP archive in MinIO"""
    logger.info(f"Downloading and extracting {object_name} from MinIO bucket {bucket_name}")
    os.makedirs(local_dir, exist_ok=True)

    # Initialize S3 client
    s3_client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )

    # Add x-minio-extract header for ZIP extraction
    def _add_header(request, **kwargs):
        request.headers.add_header("x-minio-extract", "true")

    event_system = s3_client.meta.events
    event_system.register_first("before-sign.s3.*", _add_header)

    # Local file path where extracted data will be stored
    extracted_file_path = os.path.join(local_dir, os.path.basename(object_name).replace('.zip', ''))

    try:
        s3_client.download_file(Bucket=bucket_name, Key=object_name, Filename=extracted_file_path)
        logger.info(f"Extracted file saved to {extracted_file_path}")
    except Exception as e:
        logger.error(f"Failed to download and extract data from MinIO: {e}")
        raise

    return extracted_file_path


def get_datasets(data_dir: str):
    """Prepare MNIST datasets"""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))  # MNIST-specific normalization
    ])

    train_dataset = datasets.MNIST(
        root=data_dir,
        train=True,
        download=True,
        transform=transform
    )

    val_dataset = datasets.MNIST(
        root=data_dir,
        train=False,
        download=True,
        transform=transform
    )

    return train_dataset, val_dataset


def train_func(config: Dict[str, Any]):
    """Ray Train function for LeNet training"""

    # Initialize model
    model = LeNet(num_classes=10)

    # Prepare datasets
    train_dataset, val_dataset = get_datasets(config["data_dir"])

    train_loader = DataLoader(
        train_dataset,
        batch_size=config["batch_size"],
        shuffle=True,
        num_workers=2
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=config["batch_size"],
        shuffle=False,
        num_workers=2
    )

    # Initialize optimizer and loss function
    optimizer = optim.Adam(model.parameters(), lr=config["learning_rate"])
    criterion = nn.CrossEntropyLoss()

    for epoch in range(config["num_epochs"]):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for batch_idx, (data, target) in enumerate(train_loader):
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(output.data, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()

            if batch_idx % 100 == 0:
                logger.info(f'Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item():.4f}')

        train_accuracy = 100. * correct / total
        train_loss = running_loss / len(train_loader)

        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for data, target in val_loader:
                output = model(data)
                val_loss += criterion(output, target).item()
                _, predicted = torch.max(output.data, 1)
                val_total += target.size(0)
                val_correct += (predicted == target).sum().item()

        val_accuracy = 100. * val_correct / val_total
        val_loss = val_loss / len(val_loader)

        metrics = {
            "epoch": epoch + 1,
            "train_loss": train_loss,
            "train_accuracy": train_accuracy,
            "val_loss": val_loss,
            "val_accuracy": val_accuracy
        }

        logger.info(f"Epoch {epoch + 1}: Train Loss: {train_loss:.4f}, "
                    f"Train Acc: {train_accuracy:.2f}%, "
                    f"Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.2f}%")

        session.report(metrics)


def parse_args():
    parser = argparse.ArgumentParser(description="Train MNIST using LeNet-5")
    parser.add_argument("--data-dir", type=str, required=True, help="Path to the dataset directory")
    parser.add_argument("--minio-endpoint", type=str, required=False, help="MinIO endpoint URL")
    parser.add_argument("--minio-access-key", type=str, required=False, help="MinIO access key")
    parser.add_argument("--minio-secret-key", type=str, required=False, help="MinIO secret key")
    parser.add_argument("--minio-bucket-name", type=str, required=False, help="MinIO bucket name")
    parser.add_argument("--minio-object-name", type=str, required=False, help="MinIO object name")
    return vars(parser.parse_args())


if __name__ == "__main__":
    logger.info("Training Script Starting Up...")

    # Parse arguments
    config = parse_args()

    # If MinIO parameters are provided, download the dataset
    # if config.get("minio_endpoint"):
    #     local_data_dir = "/tmp/mnist"
    #     download_and_extract_from_minio(
    #         endpoint_url=config["minio_endpoint"],
    #         access_key=config["minio_access_key"],
    #         secret_key=config["minio_secret_key"],
    #         bucket_name=config["minio_bucket_name"],
    #         object_name=config["minio_object_name"],
    #         local_dir=local_data_dir
    #     )
    #     config["data_dir"] = local_data_dir

    # Add default training configurations
    training_config = {
        "batch_size": 64,          # Batch size
        "learning_rate": 0.001,    # Learning rate
        "num_epochs": 10,          # Number of epochs
    }
    config.update(training_config)

    # Initialize TorchTrainer
    trainer = TorchTrainer(
        train_loop_per_worker=train_func,
        train_loop_config=config,
        scaling_config=ScalingConfig(num_workers=2, use_gpu=False),
    )

    # Start training and print results
    result = trainer.fit()
    print("Training result:", result)