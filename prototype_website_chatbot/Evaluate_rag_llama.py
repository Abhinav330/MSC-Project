import os
from dotenv import load_dotenv
from tqdm import tqdm
import pandas as pd
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_verbose
from langchain.globals import set_debug

set_debug(False)
set_verbose(False)

load_dotenv()
groq_api_key= os.getenv("GROQ_API_KEY")

prompt3 = ChatPromptTemplate.from_messages(
    [
        ("system", 
         '''
         You are a helpful University assistant. Your job is to give the diffrent course information asked by the user.Answer the questions based on the provided contexts only in the given format:
         <context>
         {context}
         </context>
         In above context No_data means course is not available so please dont include it.

         response format: 
         Yes, [University Name] provides a course on [Subject name]: 
         Course title: [page_title]. 
         Campus: [campus]. 
         [If Duration of the course for full time course is available]
         
         For full-time course: 
         UK fees:[full_time_uk_fees]. 
         international fees: [full_time_international_fees]. 
         The duration of the course is [full_time_duration]. 
         For more details please visit the official website:[full_time_url] 
         
         [If Duration of the course for part time course is available]
         
         For Part-time course: 
         UK fees: [part_time_uk_fees]. 
         international fees: [part_time_international_fees]. 
         The duration of the course is [part_time_duration]. 
         For more details please visit the official website: [part_time_url]

         '''
        ),
        ("user", "Question:{input}")        
    ]
)

llm1 = ChatGroq(model_name="llama3-70b-8192", groq_api_key=groq_api_key)
llm2 = OllamaLLM(model="chatbot3")

output_parser =  StrOutputParser()

embeddings1 = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma(persist_directory="./Croma_DB_UOW", embedding_function=embeddings1)

retriever= db.as_retriever(search_type = "similarity",search_kwargs={'k':3},)

document_chain2 = create_stuff_documents_chain(llm=llm2,prompt=prompt3)
chain4 = create_retrieval_chain(retriever,document_chain2)


df =pd.read_csv("llama_test_data.csv")



y_pred = []

for i, j in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
    ans = chain4.invoke({'input': j['question']})
    y_pred.append(ans['answer'])


df1 =pd.DataFrame({"y_pred": y_pred})

df1['y_true'] = df['response']
df1['y_true'] = df1['y_true'].str.replace("\\n", "\n")
df1.head()

df1.to_csv("rag_llama_y_true_y_pred.csv",index=False)
