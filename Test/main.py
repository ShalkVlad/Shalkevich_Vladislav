import os
import requests
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):
        pass

    @staticmethod
    def draw_table(json_file, output_file):
        df = pd.read_json(json_file)

        # Table
        columns = ['name', 'gt_corners', 'rb_corners', 'mean', 'max', 'min',
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

    @staticmethod
    def draw_plots(json_file):
        df = pd.read_json(json_file)

        # Create the "plots" folder if it doesn't exist
        if not os.path.exists("plots"):
            os.makedirs("plots")

        Plot_paths = []  # Store paths of all generated plots

        # Compare different columns and draw plots
        columns_to_compare = ['mean', 'max', 'min', 'floor_mean', 'floor_max', 'floor_min',
                              'ceiling_mean', 'ceiling_max', 'ceiling_min']

        for column in columns_to_compare:
            plt.figure(figsize=(10, 6))
            plt.plot(df['name'], df[column])
            plt.xlabel('Name')
            plt.ylabel(column.capitalize())
            plt.title(f'{column.capitalize()} Comparison')
            plt.xticks(rotation=90)

            # Save the plot with a unique filename
            plot_path = f'plots/{column}_plot.png'
            plt.savefig(plot_path)
            Plot_paths.append(plot_path)

            plt.close()

        return Plot_paths


json_file_url = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
json_file_path = 'deviation.json'
output_file_path = 'output.xlsx'

# Download JSON file
Plotter.download_json(json_file_url, json_file_path)

# Call function to draw table and save the result
Plotter.draw_table(json_file_path, output_file_path)

# Call the draw_plots method and get the plot paths
plot_paths = Plotter.draw_plots(json_file_path)

# Print the paths of all generated plots
for path in plot_paths:
    print(f"Plot saved: {path}")
