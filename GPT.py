import time
from langchain.vectorstores import Pinecone
import pinecone
from langchain.vectorstores import chroma
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import create_extraction_chain
import os
# Vector Store and retrievals
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import chroma
from langchain.chains import create_extraction_chain, create_extraction_chain_pydantic
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate
    )

def summarize(text):
    #need to mention API Key
    llm = OpenAI(temperature=0.5,openai_api_key="")

    text_splitter = CharacterTextSplitter()
    from langchain.chains.mapreduce import MapReduceChain
    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts[:3]]
    template=f"""
              please provide a summary in 150 or 200 words 
                """
    system_message_prompt_map = SystemMessagePromptTemplate.from_template(template)
    human_template="Transcript:{text} "
    human_message_prompt_map = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt_combine = ChatPromptTemplate.from_messages(messages=[system_message_prompt_map, human_message_prompt_map])
    chain = load_summarize_chain(llm=llm,
                                 chain_type="map_reduce",
                                 combine_prompt=chat_prompt_combine,
                                  verbose=True,

                                )
    summarizetext = chain.run(docs)
    return summarizetext,





    # print("adding vectordb ------------------>")
    # adding_data_to_vectordb(summarizetext)


    # schema = {
    #     "properties": {
    #         "topic": {"type": "string"},
    #         "description": {"type": "string"}},
    # }
    # chain1 = create_extraction_chain(schema, llm3)
    # final_resp=chain1.run(topics_found)
    #




def find_topics(text):
   
    from langchain.chains import create_extraction_chain, create_extraction_chain_pydantic
    #need to mention API Key
    llm3 = ChatOpenAI(temperature=0.3,
                      openai_api_key=os.getenv('OPENAI_API_KEY', ""),
                      model_name="gpt-3.5-turbo-0613",
                      request_timeout=180
                      )

    topics_text=text
    text_splitter1 = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " "], chunk_size=10000, chunk_overlap=2200)
    docs1 = text_splitter1.create_documents([topics_text])
    print(docs1)

    template1 = f"""
       find the most relevant,appropriate and suitable one line defined topic from the given text .
      """
    system_message_prompt_map1 = SystemMessagePromptTemplate.from_template(template1)

    human_template1 = "Transcript: {text}"  # Simply just pass the text as a human message
    human_message_prompt_map1 = HumanMessagePromptTemplate.from_template(human_template1)

    chat_prompt_combine1 = ChatPromptTemplate.from_messages(
        messages=[system_message_prompt_map1, human_message_prompt_map1])
    chain1 = load_summarize_chain(llm3,
                                 chain_type="map_reduce",
                                 combine_prompt=chat_prompt_combine1,
                                 verbose=True
                                 )

    topics= chain1.run({"input_documents":docs1 })
    return topics






