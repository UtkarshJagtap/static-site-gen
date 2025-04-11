from enum import Enum
from typing import List

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_text_nodes
from textnode import TextNode, TextType, text_node_to_html_node
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown)-> list[str]:

    blocks = []
    splited = markdown.split("\n\n")
    for block in splited:
        block = block.strip()
        if block =="":
            continue
        blocks.append(block)
    return blocks

def block_to_block_type(textblock: str) -> BlockType:

    if textblock.startswith(("# ","## ", "### ", "#### ", "##### ", "###### ")): 
        return BlockType.HEADING
    
    if textblock.startswith("```") and textblock.endswith("```"):
        return BlockType.CODE
    
    if textblock.startswith(">"):
        splited = textblock.split("\n")
        flag = 0
        for line in splited:
            if line.startswith(">"):
                flag += 1
        if flag == len(splited):
            return BlockType.QUOTE

    if textblock.startswith("-"):
        splited = textblock.split("\n")
        flag = 0
        for line in splited:
            if line.startswith("-"):
                flag += 1
        if flag == len(splited):
            return BlockType.UNORDERED_LIST

    if textblock.startswith("1. "):
        splited = textblock.split("\n")
        flag = 0
        length = len(splited)
        for i in range(1,length):
            if splited[i].startswith(f"{i+1}. "):
                flag += 1
        if flag == len(splited) -1:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    rawblocks = markdown_to_blocks(markdown)

    blocks_to_htmlnodes = []
    for block in rawblocks:
        typeofblock = block_to_block_type(block)
        node = blocktype_to_htmlnode(block, typeofblock)
        blocks_to_htmlnodes.append(node)
    return ParentNode(tag = "div", children= blocks_to_htmlnodes)

        

def blocktype_to_htmlnode(block: str, typeofblock: BlockType) :

    match typeofblock:

        case BlockType.PARAGRAPH:

            splited = block.split("\n")
            joined = " ".join(splited)            
            children = text_to_htmlnodes(joined)
            return ParentNode(tag = "p", children=children) 
        
        case BlockType.CODE:

            textnode = TextNode(text= block[4:-3], text_type=TextType.CODE) 
            leafnode = text_node_to_html_node(textnode) 
            parentnode = ParentNode(tag = "pre", children=[leafnode])
            return parentnode

        case BlockType.QUOTE:
            splited = block.split("\n")
            splitedandstripped = []
            for each in splited:
                if not each.startswith(">"):
                    raise ValueError("Invalid quote block")
                splitedandstripped.append(each.lstrip("> "))
            joined = " ".join(splitedandstripped) 
            children = text_to_htmlnodes(joined)
            return ParentNode(tag ="blockquote", children= children )

        case BlockType.HEADING:

            level = 0
            for char in block:
                if char == "#":
                    level += 1
            if level > 6 or level < 1:
                raise ValueError(f"Invalid heading level: {level}")

            text = block[level+1:]
            children = text_to_htmlnodes(text)
            return ParentNode(tag = f"h{level}", children= children)

        case BlockType.ORDERED_LIST:

            splited = block.split("\n")
            children = []
            for items in splited:
                listelements = text_to_htmlnodes(items[3:])
                children.append(ParentNode(tag = "li", children=listelements))
            return ParentNode(tag = "ol", children= children)

        case BlockType.UNORDERED_LIST:

            splited = block.split("\n")
            children = []
            for items in splited:
                listelements = text_to_htmlnodes(items[2:])
                children.append(ParentNode(tag = "li", children=listelements))
            return ParentNode(tag = "ul", children= children)

                    
           

def text_to_htmlnodes(text):
    leaves: List[LeafNode] = []
    textnodes = text_to_text_nodes(text)
    for textnode in textnodes:
        leaves.append(text_node_to_html_node(textnode))
    return leaves
    






