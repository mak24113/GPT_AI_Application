import time
import selenium
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
global new


#This function will filter the text and according to the given keywords
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


if __name__ == "__main__":
    driver = webdriver.Edge()
    # This is the input section
    enterurls = input("enter the urls you want to search comma seperated")
    list_in_urls = enterurls.split(",")
    # list_in_urls="""www.livemint.com,thewire.in,www.zeebiz.com,economictimes.indiatimes.com,thehindu.com,indianexpress.com,in.mashable.com,timesofindia.indiatimes.com,www.nytimes.com,www.indiatoday.in,indianexpress.com,www.forbes.com,www.indiatoday.in
    # """.split(',')
    enterkeywords = input("enter keywords comma seperated")
    keywords = enterkeywords.split(",")
    enterquery = input("enter query comma seperated")
    # This section will find the news article based on the selected time
    print("select the time--------------->\n")
    print("1.Past hour \n")
    print("2.Past 24 hours\n")
    print("3.Past week\n")
    print("4.Past month\n")
    print("5.Past Year\n")
    time_selected = int(input("enter the index from above time"))
    driver.get(f"http://www.google.com/search?q={enterquery}")
    new = []
    for i in driver.find_elements(By.TAG_NAME, "a"):
        if i.text == "News":
            new.append(i)
            break
    new[0].click()
    driver.find_element(By.ID, "hdtb-tls").click()
    time.sleep(2)
    times_ele = driver.find_element(By.CLASS_NAME, "hdtb-mn-hd").click()
    time.sleep(1)
    timesdiv = driver.find_element(By.ID, "lb")
    times = timesdiv.find_elements(By.TAG_NAME, "a")
    n_times = []
    for i in times:
        n_times.append(i)
    times_name = ['Past hour', 'Past 24 hours', 'Past week', 'Past month', 'Past year', 'Custom range']
    time_dictionary = dict(zip(n_times[:-1], times[:-1]))
    list(time_dictionary.values())[time_selected - 1].click()
    time.sleep(5)
    # This dict will store the list of news urls based on the provide query
    news_urls = {}
    lit = driver.find_elements(By.CLASS_NAME, "WlydOe")
    for i in lit:
        news_urls[i.get_attribute("href").split("//")[1].split("/")[0]] = i.get_attribute("href")

    # This part will filter the news urls from the news tab that has the same Url provided in urls list
    final_url = []
    for url in news_urls.keys():
        if url in list_in_urls:
            final_url.append(news_urls[url])

    # print(final_url)
    # ele = search.find_elements(By.XPATH, """//*[@id="bqHHPb"]/g-sticky-content/div/div/div/div/div/div/div[1]/a""")
    for i in final_url:  #
        news_urls_li = list(news_urls.values())

    obj_list = []
    for i in range(len(final_url)):
        driver.get(final_url[i])
        # print("Link",news_urls_li[i])
        txt = str(driver.find_elements(By.TAG_NAME, "body")[0].text)
        content_text = find_content(keywords, txt)
        link = final_url[i]
        list_obj = {"link": str(link),"content": content_text}
        obj_list.append(list_obj)
    print(obj_list)
    selected_obj_index = input("enter the index of the links that needs to be selected comma seperated")
    selected_ind_list = selected_obj_index.split(',')

    # This part will then summarize the selected article and store it in the report format
    with open('final_report.txt', 'a', encoding="utf-8") as file:
        for i in selected_ind_list:
            text = obj_list[int(i) - 1]['content']
            file.write("Article:---->" + obj_list[int(i) - 1]['link'])
            file.write("\n")
            file.write("Topic:---->   " + obj_list[int(i) - 1]['content'])
            file.write("\n")
