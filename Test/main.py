import requests
import pandas as pd
from tabulate import tabulate


class Plotter:
    def __init__(self):
        pass

    @staticmethod
    def draw_table(json_file, output_file):
        df = pd.read_json(json_file)

        # Table
        columns = ['name', 'gt_corners', 'mean', 'max', 'min',
                   'floor_mean', 'floor_max', 'floor_min', 'ceiling_mean',
                   'ceiling_max', 'ceiling_min']
        df = df[columns]

        table = tabulate(df, headers='keys', tablefmt='fancy_grid')

        # Saving Excel
        df.to_excel(output_file, index=False)

        print(table)
        print(f"The result is saved in a file: {output_file}")

    @staticmethod
    def download_json(url, output_file):
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_file, 'wb') as file:
                file.write(response.content)
            print(f"JSON file downloaded successfully: {output_file}")
        else:
            print(f"Failed to download JSON file. Status code: {response.status_code}")


json_file_url = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
json_file_path = 'deviation.json'
output_file_path = 'output.xlsx'

# Download JSON file
Plotter.download_json(json_file_url, json_file_path)

# Call function and save the result
Plotter.draw_table(json_file_path, output_file_path)
