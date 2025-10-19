import os
json_data = "backend/json"
def delete_data():   
    for filename in os.listdir(json_data):
        file_path = os.path.join(json_data, filename)
        if os.path.isfile(file_path) and filename.endswith(".json"):
            with open(file_path, "w", encoding="utf-8") as f:
                f.truncate(0)