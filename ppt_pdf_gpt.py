from pptx import Presentation
import os
import GPT
from PyPDF2 import PdfReader
import files_extractor


if __name__ == "__main__":
    keywords=input("Enter Keywords comma seperated")
    list_of_keywords=keywords.split(",")
    files_dir_path="."
    for file in [files_dir_path+'/'+filename for filename in os.listdir(files_dir_path) if os.path.isfile(files_dir_path+'/'+filename)]:

        if str(file).endswith(".pdf"):
            text=files_extractor.get_pdf_text(file)
        if str(file).endswith(".ppt"):
            text = files_extractor.get_ppt_text(file)

        refined_content=files_extractor.find_content(list_of_keywords,text)
        topic = GPT.find_topics(refined_content)
        with open('final_report.txt', 'a', encoding="utf-8") as file:
            summarized_text = GPT.summarize(text)
            file.write("Topic:---->   " +str(topic))
            file.write("\n")
            file.write("Summary:---->" + str(summarized_text)[4:])
            file.write("\n")
            file.write("\n")
