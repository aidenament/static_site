from htmlnode import *
from textnode import *
from markdownblock import *
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case TextType.PDF:
            return LeafNode(tag="iframe", value="", props={
                "src": text_node.url, 
                "width": "100%", 
                "height": "100%", 
                "style": "border: none;"
            })
        case _:
            raise ValueError(f"Unsupported text type: {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter is None:
        raise ValueError("delimeter cannot be None")
    if delimiter == "":
        raise ValueError("delimiter cannot be empty string")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        adds = node.text.split(delimiter)
        for i in range(len(adds)):
            if (((i % 2) == 0) and (len(adds[i]) != 0)):
                new_nodes.append(TextNode(adds[i], TextType.TEXT))
            elif (i%2) == 1:
                new_nodes.append(TextNode(adds[i], text_type))
                
    return new_nodes

def extract_markdown_images(text):
    link_names = re.findall(r"\[(.*?)\]", text)
    link_urls = re.findall(r"\((.*?)\)", text)
    return zip(link_names, link_urls)

def split_nodes_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        if not old_node.text:  # Handle empty text case
            continue
            
        # Find all image occurrences using regex
        text = old_node.text
        image_matches = list(re.finditer(r'!\[(.*?)\]\((.*?)\)', text))
        
        if not image_matches:
            # No images found, keep the node as-is
            new_nodes.append(old_node)
            continue
        
        # Process text and insert image nodes
        last_end = 0
        for match in image_matches:
            # Add text before the image
            if match.start() > last_end:
                new_nodes.append(TextNode(text[last_end:match.start()], TextType.TEXT))
                
            # Add the image node
            alt_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            last_end = match.end()
        
        # Add any remaining text after the last image
        if last_end < len(text):
            new_nodes.append(TextNode(text[last_end:], TextType.TEXT))
    
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        if not node.text:  # Handle empty text case
            continue
            
        # Use regex to find link patterns [text](url) but not image patterns ![text](url)
        parts = []
        last_end = 0
        # Modified regex to exclude image markdown by checking there's no ! before [
        for match in re.finditer(r'(?<!!)\[(.*?)\]\((.*?)\)', node.text):
            if match.start() > last_end:
                # Add text before the match
                parts.append((node.text[last_end:match.start()], None, None))
            # Add the link with text and URL
            parts.append((match.group(1), TextType.LINK, match.group(2)))
            last_end = match.end()
        
        # Add any remaining text after the last match
        if last_end < len(node.text):
            parts.append((node.text[last_end:], None, None))
        
        # Create TextNodes from the parts
        for text, text_type, url in parts:
            if text_type == TextType.LINK:
                new_nodes.append(TextNode(text, text_type, url))
            elif text:  # Only add non-empty text nodes
                new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes

def split_nodes_pdfs(old_nodes):
    """
    Parse HTML-like PDF embed tags and convert them to PDF TextNodes.
    Looks for patterns like: <embed src="path/to/file.pdf" type="application/pdf">
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        if not old_node.text:  # Handle empty text case
            continue
            
        # Find all PDF embed occurrences using regex
        text = old_node.text
        pdf_matches = list(re.finditer(r'<embed\s+src="([^"]+)"\s+[^>]*type="application/pdf"[^>]*>', text))
        
        if not pdf_matches:
            # No PDFs found, check alternate format
            pdf_matches = list(re.finditer(r'<embed\s+src="([^"]+\.pdf)"[^>]*>', text))
            
        if not pdf_matches:
            # No PDF embeds found, keep the node as-is
            new_nodes.append(old_node)
            continue
        
        # Process text and insert PDF nodes
        last_end = 0
        for match in pdf_matches:
            # Add text before the embed
            if match.start() > last_end:
                new_nodes.append(TextNode(text[last_end:match.start()], TextType.TEXT))
                
            # Add the PDF node
            url = match.group(1)
            new_nodes.append(TextNode("", TextType.PDF, url))
            
            last_end = match.end()
        
        # Add any remaining text after the last embed
        if last_end < len(text):
            new_nodes.append(TextNode(text[last_end:], TextType.TEXT))
    
    return new_nodes

def apply_delimiter_to_all_nodes(nodes, delimiter, text_type):
    """Apply delimiter formatting to all nodes, including links and images."""
    result = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            # For text nodes, use the existing split_nodes_delimiter function
            result.extend(split_nodes_delimiter([node], delimiter, text_type))
        elif node.text_type in [TextType.LINK, TextType.IMAGE]:
            # For links and images, apply formatting to their text content
            # We need to preserve the URL
            parts = node.text.split(delimiter)
            if len(parts) > 1:  # If there's at least one delimiter
                for i in range(len(parts)):
                    if i % 2 == 0 and parts[i]:  # Text outside delimiter
                        result.append(TextNode(parts[i], node.text_type, node.url))
                    elif i % 2 == 1:  # Text inside delimiter - apply formatting
                        # Create a new node with both the link/image type and the formatting
                        # We're keeping the URL from the original node
                        formatted_node = TextNode(parts[i], text_type, node.url if i == 0 else None)
                        result.append(formatted_node)
            else:
                # No delimiter found, keep the node as is
                result.append(node)
        else:
            # For other node types, keep them as they are
            result.append(node)
    return result

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    # First process links, images, and PDFs
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_pdfs(nodes)
    
    # Process formatting on all nodes, including link text
    for j in range(len(nodes)):
        node = nodes[j]
        if node.text_type in [TextType.LINK, TextType.IMAGE]:
            # For link/image nodes, we need to process the text content for formatting
            # but keep the node type and URL
            link_text = node.text
            link_url = node.url
            link_type = node.text_type
            
            # Apply formatting to the link text
            temp_nodes = [TextNode(link_text, TextType.TEXT)]
            temp_nodes = split_nodes_delimiter(temp_nodes, "**", TextType.BOLD)
            temp_nodes = split_nodes_delimiter(temp_nodes, "_", TextType.ITALIC)
            temp_nodes = split_nodes_delimiter(temp_nodes, "`", TextType.CODE)
            
            # Create a new HTML node with proper formatting inside the link
            if len(temp_nodes) == 1 and temp_nodes[0].text_type == TextType.TEXT:
                # No formatting found, keep the original node
                pass
            else:
                # Replace the original node with a formatted version
                formatted_text = ""
                for temp_node in temp_nodes:
                    if temp_node.text_type == TextType.BOLD:
                        formatted_text += f"<b>{temp_node.text}</b>"
                    elif temp_node.text_type == TextType.ITALIC:
                        formatted_text += f"<i>{temp_node.text}</i>"
                    elif temp_node.text_type == TextType.CODE:
                        formatted_text += f"<code>{temp_node.text}</code>"
                    else:
                        formatted_text += temp_node.text
                
                # Update the node with formatted text
                nodes[j] = TextNode(formatted_text, link_type, link_url)
    
    # Now process regular text nodes
    new_nodes = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            processed_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            processed_nodes = split_nodes_delimiter(processed_nodes, "_", TextType.ITALIC)
            processed_nodes = split_nodes_delimiter(processed_nodes, "`", TextType.CODE)
            new_nodes.extend(processed_nodes)
        else:
            new_nodes.append(node)
    
    return new_nodes

def markdown_to_blocks(markdown):
    processed_blocks = []
    markdown = markdown.strip()
    for block in markdown.split("\n\n"):
        if len(block) != 0:
            lines = block.split("\n")
            processed_blocks.append("\n".join([line.strip() for line in lines]))
    return processed_blocks


def block_to_block_type(block):
    #check if the first 1-6 characters are # but not more than 6
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    #check if the block starts with triple backticks and ends with triple backticks
    elif block.startswith("```pdf") and block.endswith("```"):
        return BlockType.PDF
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    #if every line starts with > and there is no empty line
    elif re.match(r"^> ", block):
        return BlockType.QUOTE
    #if every line starts with - followed by a space
    elif re.match(r"^- ", block):
        return BlockType.UNORDERED_LIST
    #if every line starts with a number followed by a dot and a space
    elif re.match(r"^\d+\. ", block):
        return BlockType.ORDERED_LIST
    #otherwise normal paragraph
    else:
        return BlockType.PARAGRAPH
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case block_type.PARAGRAPH:
                children = text_to_children(block)
                nodes.append(ParentNode("p", children))
            case block_type.HEADING:
                #find the number of leading # and then generate the tag "h{num}"
                num = len(re.match(r"^#+", block).group(0))
                tag = f"h{num}"
                # Remove the # prefix from the heading text
                heading_text = block[num+1:]
                children = text_to_children(heading_text)
                nodes.append(ParentNode(tag, children))
            case block_type.CODE:
                # Strip the leading and trailing ```
                code_content = "\n".join(block.split("\n")[1:-1])
                code_node = LeafNode("code", code_content)
                nodes.append(ParentNode("pre", [code_node]))
            case block_type.PDF:
                # Strip the leading ```pdf and trailing ```
                pdf_path = block.split("\n")[1].strip()
                # Create a div to contain the iframe with explicit styling
                iframe = LeafNode(
                    "iframe", 
                    "", 
                    {
                        "src": pdf_path, 
                        "width": "100%", 
                        "height": "100%", 
                        "style": "border: none; display: block; flex: 1;"
                    }
                )
                # Create a parent container with proper class for styling
                container = ParentNode(
                    "div", 
                    [iframe], 
                    {"class": "pdf-container"}
                )
                nodes.append(container)
            case block_type.QUOTE:
                # Remove the > prefix from each line
                quote_text = "\n".join([line[2:] for line in block.split("\n")])
                children = text_to_children(quote_text)
                nodes.append(ParentNode("blockquote", children))
            case block_type.UNORDERED_LIST:
                # Split by lines and remove the - prefix
                items = [line[2:] for line in block.split("\n")]
                list_items = []
                for item in items:
                    children = text_to_children(item)
                    list_items.append(ParentNode("li", children))
                nodes.append(ParentNode("ul", list_items))
            case block_type.ORDERED_LIST:
                # Split by lines and remove the number prefix
                items = [re.sub(r"^\d+\. ", "", line) for line in block.split("\n")]
                list_items = []
                for item in items:
                    children = text_to_children(item)
                    list_items.append(ParentNode("li", children))
                nodes.append(ParentNode("ol", list_items))
            case _:
                raise ValueError(f"Unsupported block type: {block_type}")
    return ParentNode("div", nodes)

def extract_title(markdown):
    for line in markdown.split("\n"):
        match = re.match(r"^# (.*)", line)
        if match:
            return match.group(1).strip()
    
    raise ValueError("No h1 header found in markdown")
