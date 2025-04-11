from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

# image example ![rick roll](https://i.imgur.com/aKaOqIh.gif)

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]):

    result = []

    for old_node in old_nodes:

        images = extract_markdown_images(old_node.text)

        if len(images) == 0:
            result.append(old_node)
            continue

        text = old_node.text

        for image in images:
            new = text.split(f'![{image[0]}]({image[1]})', 1)
            if len(new) != 2:
                raise ValueError("invalid markdown image section is not closed")
            if new[0] != "":
                result.append(markup_text_to_textnode(new[0]))
            
            result.append(markup_image_to_textnode(image))
            text = "".join(new[1])

        if text != "":
            result.append(markup_text_to_textnode(text))
    

    return result

def split_nodes_link(old_nodes: list[TextNode]):

    result = []

    for old_node in old_nodes:

        links = extract_markdown_links(old_node.text)

        if len(links) == 0:
            result.append(old_node)
            continue

        text = old_node.text

        for link in links:
            new = text.split(f'[{link[0]}]({link[1]})', 1)
            if len(new) != 2:
                raise ValueError("invalid markdown, link section is not closed")
            if new[0] != "":
                result.append(markup_text_to_textnode(new[0]))
            
            result.append(markup_link_to_textnode(link))
            text = "".join(new[1])

        if text != "":
            result.append(markup_text_to_textnode(text))
    

    return result


def markup_text_to_textnode(text):
    return TextNode(text, TextType.TEXT)

def markup_image_to_textnode(image):
        return TextNode(image[0], TextType.IMAGE, image[1])

def markup_link_to_textnode(link):
    return TextNode(link[0], TextType.LINK, link[1])


def text_to_text_nodes(text):
    ognode = TextNode(text = text, text_type= TextType.TEXT)
    boldseparated = split_nodes_delimiter([ognode],"**", TextType.BOLD)
    italicseparated = split_nodes_delimiter(boldseparated, "_", TextType.ITALIC)
    codeseparated = split_nodes_delimiter(italicseparated, "`", TextType.CODE)
    imageseparated = split_nodes_image(codeseparated)
    result = split_nodes_link(imageseparated)
    return result

