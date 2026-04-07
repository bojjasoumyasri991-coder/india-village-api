import pandas as pd
import os

folder = r"C:\Users\sujit\OneDrive\Desktop\village_api_project\dataset"

dfs = []

for file in os.listdir(folder):

    if file.endswith(".xls") or file.endswith(".ods"):

        path = os.path.join(folder, file)

        print("Reading:", file)

        df = pd.read_excel(path)

        dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)

combined.to_csv("india_villages.csv", index=False)

print("All states merged successfully")