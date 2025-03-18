import os

def save_folder_structure(root_folder, output_file="folder_structure.txt"):
    with open(output_file, "w") as f:
        for root, dirs, files in os.walk(root_folder):
            level = root.replace(root_folder, "").count(os.sep)
            indent = " " * (level * 4)
            f.write(f"{indent}{os.path.basename(root)}/\n")
            sub_indent = " " * ((level + 1) * 4)
            for file in files:
                f.write(f"{sub_indent}{file}\n")

# Run the script for the current folder
save_folder_structure(root_folder=".")

print("✅ Folder structure saved as 'folder_structure.txt'")
