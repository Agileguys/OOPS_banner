import os
import shutil

# 1. CHANGE THIS PATH IF NEEDED
# This will work on Windows/Linux/Mac if your Downloads folder is standard.
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

# You can change it to any other folder, like:
DOWNLOADS_FOLDER = "C:\\Users\\admin\\Documents"

# 2. FILE TYPE CATEGORIES
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv"],
    "Documents": [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".txt"],
    "Music": [".mp3", ".wav", ".flac", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".c", ".cpp", ".java", ".js", ".html", ".css", ".ipynb"],
    "Installers": [".exe", ".msi", ".deb", ".rpm"],
}

# Fallback folder when extension is unknown
OTHERS_FOLDER = "Others"


def get_category(file_name: str) -> str:
    """
    Returns the folder/category name for a given file based on its extension.
    If no match is found, returns the OTHERS_FOLDER.
    """
    ext = os.path.splitext(file_name)
    ext = ext.lower()

    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category

    return OTHERS_FOLDER


def organize_folder(folder_path: str):
    """
    Organizes files in the given folder into subfolders based on file type.
    """
    if not os.path.isdir(folder_path):
        print(f"[ERROR] Folder does not exist: {folder_path}")
        return

    print(f"Organizing folder: {folder_path}\n")

    # List all items in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path,item)

        # Skip if it's a directory
        if os.path.isdir(item_path):
            continue

        category = get_category(item)
        target_folder = os.path.join(folder_path, category)

        # Create the category folder if it doesn't exist
        os.makedirs(target_folder, exist_ok=True)

        # Target path
        target_path = os.path.join(target_folder, item)

        # Handle duplicate file names
        if os.path.exists(target_path):
            base_name, ext = os.path.splitext(item)
            counter = 1
            new_name = f"{base_name}_{counter}{ext}"
            new_target_path = os.path.join(target_folder, new_name)

            while os.path.exists(new_target_path):
                counter += 1
                new_name = f"{base_name}_{counter}{ext}"
                new_target_path = os.path.join(target_folder, new_name)

            target_path = new_target_path

        # Move the file
        try:
            shutil.move(item_path, target_path)
            print(f"[MOVED] {item}  -->  {category}/")
        except Exception as e:
            print(f"[ERROR] Could not move {item}: {e}")

    print("\n✅ Organizing complete!")


if __name__ == "__main__":
    organize_folder(DOWNLOADS_FOLDER)
