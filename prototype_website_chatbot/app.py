import os
from dotenv import load_dotenv
import streamlit as st

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
set_debug(True)
set_verbose(False)

load_dotenv()
groq_api_key= os.getenv("GROQ_API_KEY")

prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system",
         '''
         User will ask you a question about a course from the university. You need to do the following things:
         1. Identify the university name from the query.
         2. Identify the subject name from the query.
         3. Identify the type of degree from the query.
         4. If asked about a person or a place then identify their industry/core field and relevent course name.
         5. If no university name is given, assume [University name] is "University of Westminster".
         6. Return the question in the following format:
         Does the [University name] offer a course on [Subject name] [Type of degree]?
         If the type of degree is not specified, use this format:
         Does the [University name] offer the course on [Subject name] for any degree?
         7. Strictly only return the question as described above. Do not write anything else.
         '''

        ),
        ("user", "Question:{query1}")        
    ]
)



prompt2 = ChatPromptTemplate.from_messages(
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
         [If full time course details are available]
         
         For full-time course: 
         UK fees:[full_time_uk_fees]. 
         international fees: [full_time_international_fees]. 
         The duration of the course is [full_time_duration]. 
         For more details please visit the official website:[full_time_url] 
         
         [If part time course details are available]
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
         Yes, [University Name] provides several course on [Subject name]:  
         ## [Course 1]:  
         **Campus:** [campus].
         **Duration of the full time course:** [full_time_duration].
         **Full time course:** [full_time_url]
         [add if available]

        **Duration of the part time course:** [part_time_duration].
         **Part time course:** [part_time_url]
        ## [Course 2]: 
         **Campus:** [campus].
         **Duration of the full time course:** [full_time_duration]. 
         **Full time course:** [full_time_url]
         [add if available]
         
         **Duration of the part time course:** [part_time_duration].
         **Part time course:** [part_time_url]
        ## [Course 3]:  
         **Campus:** [campus].
         **Duration of the full time course:** [full_time_duration].
         **Full time course:** [full_time_url]
         [add if available]
         
         **Duration of the part time course:** [part_time_duration].
         **Part time course:** [part_time_url]
        ## [Course 4]: 
         **Campus:** [campus].
         **Duration of the full time course:** [full_time_duration].
         **Full time course:** [full_time_url]
         [add if available]

         **Duration of the part time course:** [part_time_duration].
         **Part time course:** [part_time_url]
        ## [Course 5]: 
         **Campus:** [campus].
         **Duration of the full time course:** [full_time_duration].
         **Full time course:** [full_time_url]
         [add if available]
         
         **Duration of the part time course:** [part_time_duration].
         **Part time course:** [part_time_url]

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
retriever = db.as_retriever(search_type = "similarity",search_kwargs={'k':3},)
retriever1 = db.as_retriever(search_type = "similarity",search_kwargs={'k':6},)
chain1 = prompt1|llm1| output_parser

document_chain = create_stuff_documents_chain(llm=llm2,prompt=prompt2)
chain2 = create_retrieval_chain(retriever,document_chain)

document_chain1 = create_stuff_documents_chain(llm=llm1,prompt=prompt3)
chain3 = create_retrieval_chain(retriever1,document_chain1)

st.title('''An AI-Driven Solution:''')
st.subheader("University Website Assistant")
query=st.text_input("**Enter your query for any course details!**")


# if query:
#     question = chain1.invoke({"query1": query})
#     placeholder = st.empty()
#     streamed_text = ""



if query:
    question =  chain1.invoke({"query1": query})
    placeholder = st.empty()
    streamed_text = ""

    if "for any degree" in question:
        for chunk in chain3.stream({'input':question}):
            if 'answer' in chunk.keys():
                streamed_text += chunk['answer']
                formatted_text = streamed_text.replace("\n", "  \n")  
                placeholder.markdown(formatted_text)
    
    else:
        for chunk in chain2.stream({'input':question}):
            if 'answer' in chunk.keys():
                streamed_text += chunk['answer']
                formatted_text = streamed_text.replace("\n", "  \n")  
                placeholder.markdown(formatted_text)
