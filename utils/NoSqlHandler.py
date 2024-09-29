from fastapi import HTTPException
import json


class NoSqlHandler:

    @staticmethod
    def create_document(document, collection_name):

        with open(f"{collection_name}.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        doc_id = document.get("id") if document.get("id") else HTTPException(status_code=500, detail="Document ID Can't Be None")
        if doc_id not in data:
            data[doc_id] = document
        else:
            HTTPException(status_code=500, detail="Document with Specified ID Already Exists.")

        with open(f"{collection_name}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def read_document(document_id, collection_name):
        with open(f"{collection_name}.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        return data.get(document_id, None)

    @staticmethod
    def update_document(document, collection_name):
        with open(f"{collection_name}.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        data[document["id"]] = document

    @staticmethod
    def delete_document(document_id, collection_name):
        with open(f"{collection_name}.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        del data[document_id]

        with open(f"{collection_name}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def read_all(collection_name):
        with open(f"{collection_name}.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        return data
