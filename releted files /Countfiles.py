import os
import pandas as pd # type: ignore

root_path = r"/home/sahil/Desktop/MY Computer file/RohitSir_FishProject/IndianFishDistributed/Image"


all_rows = []

# Detect top-level folders (train, test, val)
top_folders = [f for f in os.listdir(root_path)
               if os.path.isdir(os.path.join(root_path, f))]

# Collect all file counts
for main_folder in top_folders:
    main_path = os.path.join(root_path, main_folder)

    for root, dirs, files in os.walk(main_path):
        if len(files) == 0:
            continue

        # Detect fish name / class name
        relative_path = os.path.relpath(root, main_path)
        if relative_path == ".":
            # files directly inside folder
            relative_path = main_folder

        fish_name = relative_path  # treat every subfolder as fish name

        all_rows.append([fish_name, main_folder, len(files)])

# Create DataFrame
df = pd.DataFrame(all_rows, columns=["Fish Name", "Main Folder", "File Count"])

# ============================== #
# ✅ Pivot so fish names vertical, folders horizontal
# ============================== #
pivot_df = df.pivot_table(index="Fish Name",
                          columns="Main Folder",
                          values="File Count",
                          aggfunc="sum",
                          fill_value=0)

# ============================== #
# ✅ Calculate percentage per column
# ============================== #
percentage_df = pivot_df.div(pivot_df.sum()) * 100

# Rename columns for clarity
percentage_df = percentage_df.add_suffix("_%")

# ============================== #
# ✅ Final merge (counts + percentages)
# ============================== #
final_df = pd.concat([pivot_df, percentage_df], axis=1)

# Sort rows alphabetically
final_df = final_df.sort_index()

print(final_df)



print("================================================\n"
      "=============================================\n"
      "===============================")

import os
import pandas as pd

root_path2 = r"/home/sahil/Desktop/MY Computer file/RohitSir_FishProject/IndianFishDistributed/Image"
# Detect top folders (train/test/val)
top_folders = [f for f in os.listdir(root_path2) if os.path.isdir(os.path.join(root_path2, f))]

raw_data = {}

# Step 1: Count files per fish in train/test/val
for folder in top_folders:
    folder_path = os.path.join(root_path2, folder)
    for sub in os.listdir(folder_path):
        sub_path = os.path.join(folder_path, sub)
        if os.path.isdir(sub_path):
            file_count = sum(len(files) for _, _, files in os.walk(sub_path))
            if sub not in raw_data:
                raw_data[sub] = {}
            raw_data[sub][folder] = file_count

# Step 2: Convert to DataFrame
df = pd.DataFrame(raw_data).T.fillna(0)

# Step 3: Calculate per-fish total
df["Total"] = df.sum(axis=1)

# Step 4: Convert raw counts to per-fish percentage (sum = 100%)
for folder in top_folders:
    df[f"{folder}_%"] = (df[folder] / df["Total"] * 100).round(2)

# Final Output - only % columns
df = df[[f"{folder}_%" for folder in top_folders]]

print(df)
