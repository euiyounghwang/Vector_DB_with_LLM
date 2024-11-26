
from langchain.text_splitter import RecursiveCharacterTextSplitter # type: ignore
from langchain.text_splitter import CharacterTextSplitter # type: ignore


some_text = """When writing documents, writers will use document structure to group content. \
    This can convey to the reader, which idea's are related. For example, closely related ideas \
    are in sentances. Similar ideas are in paragraphs. Paragraphs form a document. \n\n  \
    Paragraphs are often delimited with a carriage return or two carriage returns. \
    Carriage returns are the "backslash n" you see embedded in this string. \
    Sentences have a period at the end, but also, have a space.\
    and words are separated by space."""


def recursive():
    r_splitter = RecursiveCharacterTextSplitter(
        chunk_size=450,
        chunk_overlap=0, 
        separators=["\n\n", "\n", " ", ""]
    )

    print(r_splitter.split_text(some_text))


def character():
    c_splitter = CharacterTextSplitter(
    chunk_size=450,
    chunk_overlap=0,
    separator = ' '
    )

    print(c_splitter.split_text(some_text))


if __name__ == "__main__":
    print('\n\n')
    recursive()
    print('\n\n')
    character()