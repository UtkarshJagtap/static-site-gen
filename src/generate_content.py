import os
from os.path import isfile
from pathlib import Path
import shutil
from block_markdown import markdown_to_html_node
from htmlnode import ParentNode
 
def recurse_and_copy(source, destination):

    if os.path.lexists(destination):
        print(f"clearing{destination} ")
        shutil.rmtree(destination)

    os.mkdir(destination)

    list_of_files = os.listdir(source)

    for f in list_of_files:
        lsource = os.path.join(source,f)
        ldest = os.path.join(destination,f)

       
        if os.path.isfile(lsource):
            print(f"{lsource} is file copying to {ldest}")
            shutil.copy(lsource, ldest)
        else:
            print(f"{lsource} is directory recursing")
            recurse_and_copy(lsource, ldest)


def extract_title(markdown: str):
    splited = markdown.split("\n")


    for line in splited:
        if line.startswith("# "):
            return line.lstrip("# ").strip(" ")
    raise Exception("no header in markdown")

def generate_page(from_path, template_path, dest_path, base_path):

    with open(from_path) as f:
        print(f"reading markdown from {from_path}\n")
        markdown = f.read()

    title = extract_title(markdown)
    print(f"title extracted {title}\n")
    htmlstring = markdown_to_html_node(markdown).to_html()
    print(f"long html:\n {htmlstring}")
    
    with open(template_path) as f:
        print(f"reading tempelate from: { template_path}")
        tempelate = f.read()

    tempelate = tempelate.replace("{{ Title }}", title)
    
    tempelate = tempelate.replace("{{ Content }}", htmlstring)

    tempelate = tempelate.replace(f'href="/', f'href="{base_path}')

    tempelate = tempelate.replace(f'src="/', f'src="{base_path}')

    with open(dest_path, "w") as f:
        print(f"writing html to  {dest_path}")
        f.write(tempelate)

def generate_pages_recursive(dir_path_content, tempelate_path, dest_dir_path, base_path):
    if not os.path.lexists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok= True)

    list_of_files = os.listdir(dir_path_content)

    for file in list_of_files:
        current_file = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(current_file):
            if not Path(current_file).suffix == ".md":
                continue
            dest_path = Path(dest_path).with_suffix(".html")
            print(f"we have: {current_file} which is a file so will generate html: \n")
            generate_page(current_file, tempelate_path, dest_path, base_path)
        else:
            generate_pages_recursive(current_file, tempelate_path, dest_path, base_path)
            
            


