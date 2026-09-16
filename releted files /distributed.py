import os
import shutil
import random


# set path for folder 


folder_dir = "/home/sahil/Desktop/MY Computer file/Rohit_Fish_Projecty/BD-Freshwater-Fish Dataset"
resultf = "/home/sahil/Desktop/MY Computer file/Rohit_Fish_Projecty/IndianFishDistributed"


train_ratio = 0.78
val_ratio = 0.11
test_ratio = 0.11

# create output folder for  {resultf} like that 

for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(resultf,split), exist_ok = True)

# process each class for folder where we had contain the data 

for folder in os.listdir(folder_dir):
    folder_path = os.path.join(folder_dir, folder)
    #skip if none directories 

    if not os.path.isdir(folder_path):
        continue
    
    print(f"Processing {folder}")


    # Create subfolder in train/test/val folders for class 

    for split in ["train", "test", "val"]:
        os.makedirs(os.path.join(resultf,split,folder), exist_ok=True)
    

    # list files 
    files = [f for f in os.listdir(folder_path)
             if os.path.isfile(os.path.join(folder_path,f))]
    
    #shuffle the file for random search

    random.shuffle(files)

    total = len(files)
    train_count = int(total * train_ratio)
    val_count = int(total * val_ratio)
    test_count = total - train_count - val_count


    # split the files for all 

    train_files = files[:train_count]
    val_files = files[train_count:train_count + val_count]
    test_files = files[train_count + val_count:]


    # Function to move files each and every folder 

    def move_files (file_list, split):
        for f in file_list:
            source = os.path.join(folder_path, f)
            dst = os.path.join(resultf, split, folder, f)
            shutil.copy(source, dst)  # use for change to copy and move 
            # shutil.move(source, dst) # this is used for move and detele from original file saurce


    # Copy files for after this operation 

    move_files(train_files, "train")
    move_files(val_files, "val")
    move_files(test_files, "test")

print("Dataset distributed completed")
 