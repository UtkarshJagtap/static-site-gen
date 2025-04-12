
from generate_content import(
    generate_page,
    recurse_and_copy,
    generate_pages_recursive
)

import sys
 
def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    basepath = "/"
    dir_path_static = "./static"
    dir_path_docs = "./docs"
    dir_path_content = "./content"
    template_path = "./template.html"
    recurse_and_copy(dir_path_static, dir_path_docs)
    #generate_page(os.path.join(dir_path_content, "index.md"), template_path, os.path.join(dir_path_public, "index.html"))
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs,basepath)

    pass
    
if __name__ == "__main__":
    main()
