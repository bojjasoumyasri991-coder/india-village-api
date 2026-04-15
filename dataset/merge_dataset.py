import pandas as pd
import os

folder = "dataset"   # dataset folder inside project

dfs = []

for file in os.listdir(folder):

    if file.endswith(".xls") or file.endswith(".xlsx") or file.endswith(".ods"):

        path = os.path.join(folder, file)

        print("Reading:", file)

        try:
            df = pd.read_excel(path)

            # remove empty rows
            df = df.dropna(how="all")

            # remove duplicate columns
            df = df.loc[:, ~df.columns.duplicated()]

            dfs.append(df)

        except Exception as e:
            print("Skipping file:", file)
            print("Error:", e)

# merge all datasets
combined = pd.concat(dfs, ignore_index=True)

# save clean dataset
combined.to_csv("india_villages.csv", index=False)

print("All states merged successfully!")