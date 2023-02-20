import os
import re
import vpk
import sys
import shutil
import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

ease_of_use = "this folder is here for the sake of ease of use"
if not os.path.exists(ease_of_use):
    os.makedirs(ease_of_use)
logging.basicConfig(filename=os.path.join(ease_of_use, "error.log"), level=logging.ERROR)

def is_dir_empty(path):
    return not os.listdir(path)

gen_cont = "copy files inside this folder to your modded pak01_dir"
if os.path.exists(gen_cont):
    if not is_dir_empty(gen_cont):
        print(f"> Cleaning previous patched files...")
        shutil.rmtree(gen_cont)
        print(f"- Previous patched files removed.")
if not os.path.exists(gen_cont):
    os.makedirs(gen_cont)


script = "DOTA 2 NO BULLSHIT WARD"
# Get the path to the script file
script_path = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(script_path, ease_of_use, "database.txt")
# Check if the input file is in the same folder as the script file
file_path = os.path.join(script_path, ease_of_use, "items_game.txt")
# Set the default_ward.vmdl_c path to the same directory as the script file
vmdl_path = os.path.join(script_path, ease_of_use, "default_ward.vmdl_c")
# Define the regex pattern to search for
regex_pattern = r'"models/items/wards/[^"]*"'
# Define the replacement string
replacement_string = r'"models/props_gameplay/default_ward.vmdl"'
# Define the regex pattern to search for
regex_pattern_vmdl = r'"models/items/wards/([^/]+)'

# Message repetation
vld1 = "File selected:\npak01_dir.vpk\n\nFile path:\n"
vld2 = "\n\nClick YES to proceed to extract and patch the items_game.txt\nClick NO to change the path."
warn = "No file or invalid file is selected!\nPlease select the pak01_dir.vpk\n\nClose the command window if you want to abort the process."
det1 = "The previous pak01_dir.vpk file is detected in:\n"
det2 = "\n\nClick YES to proceed.\nClick NO to change the path."

root = tk.Tk()
root.withdraw()

if not os.path.exists(database):
    message = "Welcome to DOTA 2 NO BS WARD PATCHER by Avtera!\n\nThe file pak01_dir.vpk is not found.\nPlease locate the file."
    messagebox.showinfo(script, message)
    while True:
        # Prompt user to select input file using file dialog
        browse_file_path = filedialog.askopenfilename(title="Select pak01_dir.vpk or items_game.txt")
        if "items_game.txt" in browse_file_path:
            file_path = browse_file_path
            break
        if "pak01_dir.vpk" in browse_file_path:
            vld = f"{vld1}{browse_file_path}{vld2}"
            user_prompt = messagebox.askyesno(script, vld)
            if user_prompt:
                with open(database, "w") as f:
                    f.write(browse_file_path)
                print("> Opening pak01_dir.vpk...")
                pak01 = vpk.open(browse_file_path)
                pakfile = pak01.get_file("scripts/items/items_game.txt")
                print("> Extracting items_game.txt...")
                pakfile.save("./items_game.txt")
                print("+ File items_game.txt extracted!")
                shutil.move("items_game.txt", file_path)
                break
            else:
                continue
        else:
            messagebox.showwarning(script, warn)
            continue  # loop back to the beginning
else:
    with open(database, "r") as f:
        saved_file_path = f.read()
    message = f"{det1}{saved_file_path}{det2}"
    result = messagebox.askyesno(script, message)
    if result:
        print("> Opening pak01_dir.vpk...")
        pak01 = vpk.open(saved_file_path)
        pakfile = pak01.get_file("scripts/items/items_game.txt")
        print("> Extracting items_game.txt...")
        pakfile.save("./items_game.txt")
        print("+ File items_game.txt extracted!")
        shutil.move("items_game.txt", file_path)
    else:
        while True:
            # Prompt user to select input file using file dialog
            browse_file_path = filedialog.askopenfilename(title="Select pak01_dir.vpk or items_game.txt")
            if "items_game.txt" in browse_file_path:
                file_path = browse_file_path
                break
            if "pak01_dir.vpk" in browse_file_path:
                vld = f"{vld1}{browse_file_path}{vld2}"
                user_prompt = messagebox.askyesno(script, vld)
                if user_prompt:
                    with open(database, "w") as f:
                        f.write(browse_file_path)
                    pak01 = vpk.open(browse_file_path)
                    pakfile = pak01.get_file("scripts/items/items_game.txt")
                    pakfile.save("./items_game.txt")
                    shutil.move("items_game.txt", file_path)
                    break
                else:
                    continue
            else:
                messagebox.showwarning(script, warn)
                continue  # loop back to the beginning

# Read input string from file
with open(file_path, "r", encoding="utf-8") as f:
    file_contents = f.read()

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write(f"[{bar}] {percents}% {status}\r")
    sys.stdout.flush()

# Replace all occurrences of the regex pattern with the replacement string
try:
    new_file_contents = ""
    num_replacements = 0
    num_regex = 0
    match_iterator = re.finditer(regex_pattern, file_contents)
    total_matches = len(list(match_iterator))
    match_iterator = re.finditer(regex_pattern, file_contents)
    print("> Patching the items_game.txt...")
    for i, match in enumerate(match_iterator):
        new_file_contents += file_contents[num_replacements:match.start()]
        new_file_contents += replacement_string
        num_replacements = match.end()
        num_regex += 1
        progress(i, total_matches, f"[Items replaced: {num_regex}]")
    new_file_contents += file_contents[num_replacements:]
except Exception as e:
    message = f"Error: could not patch items_game.txt\nException message: {str(e)}"
    print(f"\n{message}")
    messagebox.showerror(script, message)
    input("Press Enter to exit...")
    exit()
if num_replacements <= 0:
    message = "Error: could not patch items_game.txt\nException message: The inserted pak01_dir.vpk file is already patched!"
    print(f"\n{message}")
    messagebox.showerror(script, message)
    input("Press Enter to exit...")
    exit()
    

# Set the output directory and filename
output_dir = os.path.join(gen_cont, "scripts", "items")
output_file = os.path.join(output_dir, "items_game.txt")
os.makedirs(output_dir, exist_ok=True)
# Write modified content to output file
try:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(new_file_contents)
        print("\n+ Patched items_game is sucessfuly saved!")
except Exception as e:
    message = f"Error: could not write output file.\nException message: {str(e)}"
    print(f"\n{message}")
    messagebox.showerror(script, message)
    input("Press Enter to exit...")
    exit()

# Search for matches in the input string
try:
    print("> Creating duplicate of default ward model...")
    matches = re.findall(regex_pattern_vmdl, file_contents)
    num_copies = 0
    # Iterate over the matches and copy/rename the default_ward.vmdl file
    for match in matches:
        # Build the source and destination paths
        dst_dir = os.path.join(gen_cont, "models", "items", "wards", match)
        dst_path = os.path.join(dst_dir, f"{match}.vmdl_c")
        # Create the destination directory if it doesn't exist
        os.makedirs(dst_dir, exist_ok=True)
        # Copy the file to the destination path
        shutil.copy(vmdl_path, dst_path)
        num_copies += 1
    print(f"+ Total {num_copies} wards model is succesfully linked!")
except Exception as e:
    message = f"Error: could not link ward model.\nException message: {str(e)}"
    print(f"\n{message}")
    messagebox.showerror(script, message)
    input("Press Enter to exit...")
    exit()

# Cleaning shit
print(f"> Cleaning chaced files...")
os.remove(file_path)
print(f"- Cached file removed.")

# Show information about the output file
print("\nClick OK to close this command window.")
message = f"{num_regex} bullshit wards reverted to the default ward.\n\nFile output directory:\n{gen_cont}\n\nThis patcher created by:\nhttps://github.com/Avtera/"
messagebox.showsuccess(script, message)