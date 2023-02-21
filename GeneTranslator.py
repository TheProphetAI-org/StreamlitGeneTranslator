import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import pyperclip

#functions
def connect():
    connection = psycopg2.connect(user="gene_db_user",
                                password="xJzyiS7igd4nqfLEiUURCXOUifHJZaRr",
                                host="dpg-cfn5smqrrk0eqluh0nug-a.frankfurt-postgres.render.com",
                                port="5432",
                                database="gene_db")
    cursor = connection.cursor()
    return cursor

def build_query(gene):
    #postgreSQL_select_Query = 'SELECT "GeneSym", "UniprotID" FROM public."GeneTab" WHERE "UniprotID"=\'{}\''
    query ='SELECT "GeneSymbol" FROM public."GeneTab_Full" WHERE \'{}\' in ("GeneSymbol","UniprotID","BioGRID","ChEMBL","ComplexPortal","DIP","DrugBank","GO","String") LIMIT 1'.format(gene)
    return query

def preprocess_text_input(text):
    special_characters=['@','#','$','*','&']
    delimiters=[',',';','|']
    text=text.upper()
    for i in special_characters:
        text=text.replace(i,'')
    for j in delimiters:
        text=text.replace(j,' ')
    df = pd.DataFrame([s.strip() for s in text.split()])#.transpose()
    return df

#APP

#Input section
st.title('GeneTranslator')
st.text("Enter one of more IDs. Separate IDs by whitespace (space, tab, newline)")
text=st.text_area(label="Insert Here Your Genes")

#Buttons
col1,col2= st.columns(2)
bt=col1.button("Translate", key=1)
placeholder= col2.empty()

df=preprocess_text_input(text)
cursor=connect()


if bt:
    genetext=""
    gene_org=""
    placeholder.write(f"⏳")
    my_bar = st.progress(0)
    for index, row in df.iterrows():
        my_bar.progress(index/len(df)+1/len(df))
        try:
            cursor.execute(build_query(row[0]))
        except:
            st.write("Error: Please reload the page")
        selection = cursor.fetchall()
        result = pd.DataFrame(selection)
        print(result)
        #col1.text(row[0])
        gene_org=gene_org+"\n"+ row[0]
        try:
            #col2.text(result[0].values[0])
            genetext=genetext+"\n"+ result[0].values[0]
        except:
            genetext=genetext+"\n"+ "na"
            #col2.text('na')
    
if 'genetext' in locals():
    col1.text(gene_org)
    col2.text(genetext)
    cpbt=placeholder.button("Copy to clipboard", on_click=pyperclip.copy(genetext),key=2)

