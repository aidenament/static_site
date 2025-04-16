from textnode import TextNode, TextType
from funcs import markdown_to_html_node, extract_title
import os
import shutil

def recursive_copy(source_path, destination_path):
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    
    # Create the destination directory
    os.makedirs(destination_path)
    
    # Iterate through all items in the source directory
    for item in os.listdir(source_path):
        source_item_path = os.path.join(source_path, item)
        destination_item_path = os.path.join(destination_path, item)
        
        if os.path.isdir(source_item_path):
            # If it's a directory, recursively copy it
            print(f"Copying directory: {source_item_path} -> {destination_item_path}")
            recursive_copy(source_item_path, destination_item_path)
        else:
            # If it's a file, copy it
            print(f"Copying file: {source_item_path} -> {destination_item_path}")
            shutil.copy2(source_item_path, destination_item_path)

def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from a markdown file using a template.
    
    Args:
        from_path: Path to the markdown file
        template_path: Path to the template file
        dest_path: Path where the generated HTML file will be saved
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title from markdown, use filename as fallback
    try:
        title = extract_title(markdown_content)
    except ValueError:
        # Use the filename without extension as the fallback title
        basename = os.path.basename(from_path)
        title = os.path.splitext(basename)[0].capitalize()
        print(f"Warning: No H1 header found in {from_path}, using '{title}' as title")
    
    # Replace placeholders in template
    filled_template = template_content.replace("{{ Title }}", title)
    filled_template = filled_template.replace("{{ Content }}", html_content)
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the filled template to the destination path
    with open(dest_path, 'w') as f:
        f.write(filled_template)

def generate_pages_recursive(content_dir, template_path, public_dir):
    """
    Recursively generate HTML pages from markdown files in the content directory.
    
    Args:
        content_dir: Path to the content directory
        template_path: Path to the template file
        public_dir: Path to the public directory where HTML files will be saved
    """
    for item in os.listdir(content_dir):
        content_path = os.path.join(content_dir, item)
        
        # Skip hidden files or directories
        if item.startswith('.'):
            continue
            
        if os.path.isdir(content_path):
            # Recursively process subdirectories
            generate_pages_recursive(content_path, template_path, public_dir)
        elif item.endswith('.md'):
            # Process markdown file
            # Determine the output path by replacing content_dir with public_dir
            # and changing .md extension to .html
            rel_path = os.path.relpath(content_path, 'content')
            if item == "index.md":
                # For index.md files, keep the directory structure but use index.html
                dest_path = os.path.join(public_dir, os.path.dirname(rel_path), 'index.html')
            else:
                # For other markdown files, create a directory with an index.html file
                dest_path = os.path.join(public_dir, os.path.splitext(rel_path)[0], 'index.html')
            
            generate_page(content_path, template_path, dest_path)

def main():
    # Clean public directory (will be recreated by recursive_copy)
    if os.path.exists("public"):
        shutil.rmtree("public")
    
    # Copy static files to public directory
    recursive_copy("static", "public")
    
    # Generate pages from all markdown files in the content directory
    generate_pages_recursive('content', 'template.html', 'public')
    
    print("Site generation complete!")

main()
