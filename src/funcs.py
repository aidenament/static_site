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
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        if not node.text:  # Handle empty text case
            continue
            
        # Use regex to find image patterns ![alt](url)
        parts = []
        last_end = 0
        for match in re.finditer(r'!\[(.*?)\]\((.*?)\)', node.text):
            if match.start() > last_end:
                # Add text before the match
                parts.append((node.text[last_end:match.start()], None, None))
            # Add the image with alt text and URL
            parts.append((match.group(1), TextType.IMAGE, match.group(2)))
            last_end = match.end()
        
        # Add any remaining text after the last match
        if last_end < len(node.text):
            parts.append((node.text[last_end:], None, None))
        
        # Create TextNodes from the parts
        for text, text_type, url in parts:
            if text_type == TextType.IMAGE:
                new_nodes.append(TextNode(text, text_type, url))
            elif text:  # Only add non-empty text nodes
                new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        if not node.text:  # Handle empty text case
            continue
            
        # Use regex to find link patterns [text](url)
        parts = []
        last_end = 0
        for match in re.finditer(r'\[(.*?)\]\((.*?)\)', node.text):
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

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes


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
