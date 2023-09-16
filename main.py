import time
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import create_extraction_chain
import os
from langchain import OpenAI
from  vectordb import add_docs_to_vectordb
from GPT import summarize,find_topics
# Vector Store and retrievals
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import chroma
from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate
    )

from langchain.chains.question_answering import load_qa_chain
import selenium
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
driver=webdriver.Edge()
enterurls=input("enter the urls you want to search comma seperated")
list_in_urls=enterurls.split(",")
# list_in_urls="""www.livemint.com,thewire.in,www.zeebiz.com,economictimes.indiatimes.com,thehindu.com,indianexpress.com,in.mashable.com,timesofindia.indiatimes.com,www.nytimes.com,www.indiatoday.in,indianexpress.com,www.forbes.com,www.indiatoday.in
# """.split(',')

#print(list_in_urls)
enterkeywords=input("enter keywords comma seperated")
#
# keywords='charts,stock price,stock value,Last traded price,profit,research,graphs'
keywords=enterkeywords.split(",")


#print(keywords)
enterquery=input("enter query comma seperated")
# # query=enterquery
# query="stock price analysis for previous quarter in 2023-2024 for infosys "
#print(query)



print("select the time--------------->\n")
print("1.Past hour \n")
print("2.Past 24 hours\n")
print("3.Past week\n")
print("4.Past month\n")
print("5.Past Year\n")

time_selected=int(input("enter the index from above time"))

driver.get(f"http://www.google.com/search?q={query}")


global new
new=[]
for i in driver.find_elements(By.TAG_NAME,"a"):
    if i.text=="News":
        new.append(i)
        break
new[0].click()
driver.find_element(By.ID,"hdtb-tls").click()
time.sleep(6)
times_ele=driver.find_element(By.CLASS_NAME,"hdtb-mn-hd").click()
time.sleep(10)
timesdiv=driver.find_element(By.ID,"lb")

times=timesdiv.find_elements(By.TAG_NAME,"a")
n_times=[]
for i in times:
    n_times.append(i)




times_name=['Past hour','Past 24 hours','Past week','Past month','Past year','Custom range']

time_dictionary = dict(zip(n_times[:-1], times[:-1]))

#print(time_dictionary)
list(time_dictionary.values())[time_selected-1].click()

time.sleep(10)

news_urls={}
# pages_link_el=driver.find_element(By.TAG_NAME,'tbody')
# # for page_a in pages_link_el.find_elements(By.TAG_NAME,'a'):
# #     print(page_a.text)
# pages_link=[page_a for page_a in pages_link_el.find_elements(By.TAG_NAME,'a')]
#


#for page in range(1,number_pages):
    # print(pages_link[page])
    # driver.get(pages_link[page].get_attribute('href'))
lit=driver.find_elements(By.CLASS_NAME,"WlydOe")
for i in lit:
    news_urls[i.get_attribute("href").split("//")[1].split("/")[0]]=i.get_attribute("href")



# print(news_urls)
# print(len(list(news_urls.values())))
    #print(i.get_attribute("href").split("//")[1].split("/")[0])

final_url=[]
for url in news_urls.keys():
    if url in list_in_urls:
        final_url.append(news_urls[url])

#print(final_url)
# ele = search.find_elements(By.XPATH, """//*[@id="bqHHPb"]/g-sticky-content/div/div/div/div/div/div/div[1]/a""")
for i in final_url:#
    news_urls_li=list(news_urls.values())

file_path='./store'

def find_content(keywords,text):
    content = []
    with open("content.txt",'w',encoding="utf-8") as f:
        f.writelines(text)
    lines=[]
    with open("content.txt",'r',encoding="utf-8") as file:
        lines=file.readlines()
        # print(lines)
    for line in lines:
        for keyword in keywords:
            if keyword.lower() in list(line.split(" ")):
                if line not in content:
                    # print(f"upadated in text-----------------{line}")
                    content.append(line)
            elif keyword.title() in list(line.split(" ")):
                if line not in content:
                    # print(f"upadated in text-----------------{line}")
                    content.append(line)
            elif keyword.upper() in list(line.split(" ")):
                if line not in content:
                    # print(f"upadated in text-----------------{line}")
                    content.append(line)

    return "".join(content)



obj_list=[]
for i in range(len(final_url)):
    driver.get(final_url[i])
    # print("Link",news_urls_li[i])
    txt = str(driver.find_elements(By.TAG_NAME, "body")[0].text)
    content_text = find_content(keywords, txt)

    topic = find_topics(content_text)
    link = final_url[i]
    list_obj = {"link": str(link), "topic": topic,  "content": content_text}
    obj_list.append(list_obj)


for obj in obj_list:
    print(f"{obj_list.index(obj)+1}----------> {obj}")

selected_obj_index=input("enter the index of the links that needs to be selected comma seperated")
selected_ind_list=selected_obj_index.split(',')

for i in selected_ind_list:
    text=obj_list[int(i)-1]['content']
    print(summarize(text))
