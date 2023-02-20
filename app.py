import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import pyperclip

connection = psycopg2.connect(user="gene_db_user",
                                password="xJzyiS7igd4nqfLEiUURCXOUifHJZaRr",
                                host="dpg-cfn5smqrrk0eqluh0nug-a.frankfurt-postgres.render.com",
                                port="5432",
                                database="gene_db")
cursor = connection.cursor()
#postgreSQL_select_Query = 'SELECT "GeneSym", "UniprotID" FROM public."GeneTab" WHERE "UniprotID"=\'{}\''
postgreSQL_select_Query2 = 'SELECT "GeneSymbol" FROM public."GeneTab_Full" WHERE \'{}\' in ("GeneSymbol","UniprotID","BioGRID","ChEMBL","ComplexPortal","DIP","DrugBank","GO","String") LIMIT 1'


#APP
st.title('GeneTranslator')
st.text("Enter one of more IDs (100,000 max). Separate IDs by whitespace (space, tab, newline)")
text=st.text_area(label="Insert Here Your Genes")

text=text.upper()
df = pd.DataFrame([text.split()]).transpose()
col1,col2= st.columns(2)
bt=col1.button("Translate", key=1)
placeholder= col2.empty()
placeholder.write(f"⏳")

if bt:
    genetext=""
    for index, row in df.iterrows():
        
        cursor.execute(postgreSQL_select_Query2.format(row[0]))
        selection = cursor.fetchall()
        print(selection)
        result = pd.DataFrame(selection)
        try:
            col1.text(row[0])
        except:
            col1.text(row[0])
        try:
            col2.text(result[0].values[0])
            genetext=genetext+"\n"+ result[0].values[0]
        except:
            col2.text('na')
        
    copy_bt=placeholder.button("Copy to clipboard", on_click=pyperclip.copy(genetext), key=2)

