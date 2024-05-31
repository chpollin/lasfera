#!/usr/bin/python

import json

import numpy as np
import pandas as pd

filepath = "~/Downloads/lasfera.xlsx"
sheet_name = "Universal"

xls = pd.ExcelFile(filepath)

if sheet_name:
    df = pd.read_excel(xls, sheet_name, header=1)
    df = df.replace({np.nan: None})
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    dfs = {sheet_name: df}
else:
    dfs = pd.read_excel(xls, sheet_name=None, header=1)
    for sheet_name, df in dfs.items():
        df = df.replace({np.nan: None})
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        dfs[sheet_name] = df

data = []
existing_libraries = set()
for sheet_name, df in dfs.items():
    for index, row in df.iterrows():
        library_city = row.get("city")
        library_name = row.get("library")

        # Create a unique identifier for each library
        library_id = f"{library_name}-{library_city}"

        # Only add the library if it's not already in the set
        if library_id not in existing_libraries:
            existing_libraries.add(library_id)
            data.append(
                {
                    "model": "manuscript.Library",
                    "pk": index + 1,
                    "fields": {"library": library_name, "city": library_city},
                }
            )

with open("manuscript/fixtures/libraries.json", "w", encoding="utf-8") as f:
    json.dump(data, f)
