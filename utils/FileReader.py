# FileReader.py

from abc import ABC, abstractmethod
import json


class FileReader(ABC):
    """Base class for file readers."""

    @staticmethod
    @abstractmethod
    def read(file_name: str):
        """Read File"""
        pass

    @staticmethod
    @abstractmethod
    def write(file_name: str, data: dict):
        """Write File."""
        pass

    @staticmethod
    @abstractmethod
    def append(file_name: str, data: dict):
        """Append File."""
        pass

class JSONFileReader(FileReader):
    """Json file reader."""

    @staticmethod
    def read(file_name: str):
        """Read JSON file."""
        with open(file_name, encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def write(file_name, data: dict):
        """Write JSON file."""
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def append(file_name: str, data: dict):
        """Append Data to File."""
        with open(file_name, "a", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
