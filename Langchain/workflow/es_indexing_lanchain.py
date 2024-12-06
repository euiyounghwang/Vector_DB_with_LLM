
import json
import warnings
warnings.filterwarnings("ignore")
import os
from text_loader import loader_text


path = os.getcwd() + "/Data"


if __name__ == "__main__":
    # loader_text("test.txt", create_json=True)
    # loader_text("asiabrief_3-26.pdf", create_json=True)
    # loader_text("Sample.docx", create_json=True)
    # loader_text("Sample.doc", create_json=True)
    # loader_text("Sample.pptx", create_json=True)
    # loader_text("test", create_json=True)
    # loader_text("Sample.xls", create_json=True)
    loader_text("{}/{}".format(path, "Sample.hwp"), create_json=True)