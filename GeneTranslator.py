import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import pyperclip


#functions
def connect():
    connection = psycopg2.connect(user="gene_db_light_user",
                                password="l9KqjzIpUFh0VTfW9N6871fBxa7B2GmX",
                                host="dpg-cfuennh4reb6ks4hpit0-a.frankfurt-postgres.render.com",
                                port="5432",
                                database="gene_db_light")
    cursor = connection.cursor()
    return cursor

def build_query(gene,source):
    #postgreSQL_select_Query = 'SELECT "GeneSym", "UniprotID" FROM public."GeneTab" WHERE "UniprotID"=\'{}\''
    if source == 'All':
        query ='SELECT "genesymbol" FROM public."GeneTab_Light" WHERE \'{}\' in ("genesymbol","uniprot","biogrid","chembl","string","ensemblid","hgnc","name","ncbi","alias") LIMIT 1'.format(gene)
    else:
        query ='SELECT "genesymbol" FROM public."GeneTab_Light" WHERE "{}" = \'{}\''.format(source,gene)
        print(query)
    return query

@st.cache_data
def get_cols(_cursor):
    cursor.execute('SELECT column_name FROM information_schema.columns WHERE table_name = \'GeneTab_Light\'')
    cols=pd.DataFrame(cursor.fetchall())
    options=pd.concat([pd.DataFrame(['Select the Source','All']).append(cols)])
    return options

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

#Title
st.title('GeneTranslator')

#Connect
try:
    cursor=connect()
except:
    st.write("Error: Please reload the page")

#Input section
st.text("Enter one of more IDs. Separate IDs by whitespace (space, tab, newline)")
text=st.text_area(label="Insert Here Your Genes")
options=get_cols(cursor)
source=st.selectbox("Chose your nomenclature, if 'All' selected the system will look at all the available sources and might take some time",options)


#Buttons
output_type = st.radio("Select the output type",["GeneSymbol Only","Original Nomenclature and GeneSymbol"])
col1,col2= st.columns(2)
placeholder_bar=st.empty()
bt=col1.button("Translate", key=1)
placeholder= col2.empty()
df=preprocess_text_input(text)
col3,col4=st.columns(2)

if bt:
    genetext=""
    gene_org=pd.DataFrame()    
    placeholder.write(f"⏳")
    my_bar = placeholder_bar.progress(0)
    for index, row in df.iterrows():
        my_bar.progress(index/len(df)+1/len(df))
        try:
            cursor.execute(build_query(row[0],source))
            selection = cursor.fetchall()
            result = pd.DataFrame(selection)
        except:
            st.write("Error: Please reload the page2")
        col3.text(row[0])
        try:
            col4.text(result[0].values[0])
            genetext=genetext+"\n"+ result[0].values[0]
            gene_org=gene_org.append([[row[0],result[0].values[0]]])
        except:
            col4.text('na')
            gene_org=gene_org.append([[row[0],'na']])
    
    if output_type=="GeneSymbol Only":
        placeholder.download_button(label="Download data as txt file", data=genetext,file_name='GeneSymbol.txt',mime='text/csv',)
    else:
         placeholder.download_button(label="Download data as csv file", data=gene_org.to_csv(),file_name='OriginalandGeneSymbol.csv',mime='text/csv',)

