from textnode import *
print("hello world")
def main():
    textnode1 = TextNode("Some Bold Text", TextType.BOLD)
    textnode2 = TextNode("Some Bold Text", TextType.BOLD)
    print(textnode1)

    print(textnode1 == textnode2)


if __name__ == "__main__":
    main()
