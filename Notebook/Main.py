import os
import requests
import json

import matplotlib.pyplot as plt


class Room:
    def __init__(self):
        self.output_folder = 'plots'
        os.makedirs(self.output_folder, exist_ok=True)

    def draw_plots(self, df):
        plt.bar(df['name'], df['rb_corners']) 
        plt.xlabel('Room Name')
        plt.ylabel('Number of Corners Found by Model')
        plt.title('Number of Corners Found by Model for Each Room')
        plt.xticks(rotation=90)
        plt.savefig(os.path.join(self.output_folder, 'corners_found.png'))
        plt.close()

        return [os.path.join(self.output_folder, filename) for filename in os.listdir(self.output_folder)]


def download_json(url, save):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save, 'w') as file:
            json.dump(response.json(), file)
        print(f"JSON file downloaded successfully to {save}")
    else:
        print(f"Failed to download JSON file. Status code: {response.status_code}")


json_url = "https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json"
save_path = "deviation.json"

download_json(json_url, save_path)
