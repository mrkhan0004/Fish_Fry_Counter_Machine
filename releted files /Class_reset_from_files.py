# import os
# import glob

# def modify_class_numbers(folder_path, old_class, new_class):
#     """
#     YOLO label files mein class numbers ko modify karta hai
    
#     Args:
#         folder_path: Jis folder mein label files hain
#         old_class: Purana class number (jo change karna hai)
#         new_class: Naya class number (jo set karna hai)
#     """
#     # Folder path ko normalize karo
#     folder_path = os.path.normpath(folder_path)
    
#     # Check karo ki folder exist karta hai
#     if not os.path.exists(folder_path):
#         print(f"Error: Folder '{folder_path}' nahi mila!")
#         return
    
#     # Saari .txt files ko dhundo
#     txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    
#     if not txt_files:
#         print(f"Koi .txt files nahi mili folder mein: {folder_path}")
#         return
    
#     modified_count = 0
#     total_lines_changed = 0
    
#     print(f"Total {len(txt_files)} files milein...")
#     print(f"Class {old_class} ko {new_class} se replace kar rahe hain...\n")
    
#     for file_path in txt_files:
#         try:
#             # File ko read karo
#             with open(file_path, 'r') as f:
#                 lines = f.readlines()
            
#             # Modified lines
#             new_lines = []
#             file_changed = False
#             lines_changed_in_file = 0
            
#             for line in lines:
#                 # Empty lines ko skip karo
#                 if line.strip():
#                     parts = line.strip().split()
#                     if len(parts) >= 5:  # Valid YOLO format
#                         current_class = parts[0]
                        
#                         # Agar class match karti hai toh change karo
#                         if current_class == str(old_class):
#                             parts[0] = str(new_class)
#                             file_changed = True
#                             lines_changed_in_file += 1
                        
#                         new_lines.append(' '.join(parts) + '\n')
#                     else:
#                         new_lines.append(line)
#                 else:
#                     new_lines.append(line)
            
#             # Agar kuch change hua hai toh file ko write karo
#             if file_changed:
#                 with open(file_path, 'w') as f:
#                     f.writelines(new_lines)
                
#                 modified_count += 1
#                 total_lines_changed += lines_changed_in_file
#                 print(f"✓ Modified: {os.path.basename(file_path)} ({lines_changed_in_file} labels changed)")
        
#         except Exception as e:
#             print(f"✗ Error processing {os.path.basename(file_path)}: {str(e)}")
    
#     print(f"\n{'='*50}")
#     print(f"Summary:")
#     print(f"Total files checked: {len(txt_files)}")
#     print(f"Files modified: {modified_count}")
#     print(f"Total labels changed: {total_lines_changed}")
#     print(f"{'='*50}")

# # Main execution
# if __name__ == "__main__":
#     # Yahan apna folder path daalo
#     folder_path = r"/home/sahil/Desktop/MY Computer file/RohitSir_FishProject/IndianFishDistributed/labels/test/Black Rohu"  # Apna path yahan daalo
    
#     # Purana class number (jo change karna hai)
#     old_class = 
    
#     # Naya class number (jo set karna hai)
#     new_class = 1
    
#     print("YOLO Label Class Modifier")
#     print("="*50)
    
#     # Function ko call karo
#     modify_class_numbers(folder_path, old_class, new_class)
    
#     print("\nDone! ✓")




import os
import glob

def set_all_classes_to_new_class(folder_path, new_class):
    """
    YOLO label files mein SAARE class numbers ko ek hi class se replace karta hai
    
    Args:
        folder_path: Jis folder mein label files hain
        new_class: Naya class number jo set karna hai (saari classes ke liye)
    """
    # Folder path ko normalize karo
    folder_path = os.path.normpath(folder_path)
    
    # Check karo ki folder exist karta hai
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' nahi mila!")
        return
    
    # Saari .txt files ko dhundo
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    
    if not txt_files:
        print(f"Koi .txt files nahi mili folder mein: {folder_path}")
        return
    
    modified_count = 0
    total_lines_changed = 0
    old_classes_found = set()
    
    print(f"Total {len(txt_files)} files milein...")
    print(f"Sabhi classes ko {new_class} se replace kar rahe hain...\n")
    
    for file_path in txt_files:
        try:
            # File ko read karo
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Modified lines
            new_lines = []
            file_changed = False
            lines_changed_in_file = 0
            
            for line in lines:
                # Empty lines ko skip karo
                if line.strip():
                    parts = line.strip().split()
                    if len(parts) >= 5:  # Valid YOLO format
                        current_class = parts[0]
                        
                        try:
                            current_class_num = int(current_class)
                            old_classes_found.add(current_class_num)
                            
                            # Agar already new_class nahi hai toh change karo
                            if current_class_num != new_class:
                                parts[0] = str(new_class)
                                file_changed = True
                                lines_changed_in_file += 1
                        except ValueError:
                            pass  # Agar integer nahi hai toh skip karo
                        
                        new_lines.append(' '.join(parts) + '\n')
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            
            # Agar kuch change hua hai toh file ko write karo
            if file_changed:
                with open(file_path, 'w') as f:
                    f.writelines(new_lines)
                
                modified_count += 1
                total_lines_changed += lines_changed_in_file
                print(f"✓ Modified: {os.path.basename(file_path)} ({lines_changed_in_file} labels changed)")
        
        except Exception as e:
            print(f"✗ Error processing {os.path.basename(file_path)}: {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"Total files checked: {len(txt_files)}")
    print(f"Files modified: {modified_count}")
    print(f"Total labels changed: {total_lines_changed}")
    if old_classes_found:
        print(f"Old classes found: {sorted(old_classes_found)}")
    print(f"All changed to: {new_class}")
    print(f"{'='*60}")

# Main execution
if __name__ == "__main__":
    # Yahan apna folder path daalo
    folder_path = r"/home/sahil/Desktop/Computer/RohitSir_FishProject/IndianFishDistributed/labels/val/Nile Tilapia"
    
    # ==========================================
    # NEW CLASS - Sirf yahan apna new class number daal 
    # ==========================================
    new_class = 10


    #bhi classes ko is number se replace kar dega
    
    print("YOLO Label Class Modifier - Set All to One Class")
    print("="*60)
    
    # Function ko call karo
    set_all_classes_to_new_class(folder_path, new_class)
    
    print("\nDone! ✓")
