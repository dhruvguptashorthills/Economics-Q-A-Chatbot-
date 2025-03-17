import os
import json

def txt_files_to_json(folder_path, output_file):
    data = []

    try:
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    data.append({
                        "title": file_name,
                        "content": content
                    })

        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print(f"Data successfully written to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
folder_path = 'articles'  # Replace with the path to your folder containing .txt files
output_file = 'Data/combined_Raw_Data.json'   # Desired name for the output JSON file
txt_files_to_json(folder_path, output_file)

