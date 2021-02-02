
import streamlit as st
import streamlit.components.v1 as components
from controller.main_controller import get_table_download_link
from view.get_video import return_one_random_url
from view.display_utils import image
from view.html_variables import buy_a_coffee
from model.pubmed_api import search_query, fetch_details
from model.df_generation import DataFrameGenertion

st.header("From pubmed API to csv")

nb_publication = st.slider("Select the max number of publications you want to gather (max : 100 000 per requests, but let's put 10 000 for now)", min_value=100, max_value=10_000, step=100)

query = st.text_input("Enter a query below")

if query:
    ids_list = search_query(query, nb_publication)
    if ids_list:
        st.write("Let's watch inspirational/inspiring video while downloading")
        st.video(return_one_random_url())
        articles = fetch_details(ids_list)
        my_bar = st.progress(0)
        progressbar_max = len(articles)
        dfg = DataFrameGenertion()
        for i, article in enumerate(articles, start=1):
            my_bar.progress(i / progressbar_max)
            dfg.update_df(article)
            i += 1
        df = dfg.df
        st.dataframe(df.head())
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)
        st.image(image, caption='眠っている男', use_column_width=True)
    else:
        st.write("No articles where found with this query")

st.write("")
st.write("Made with ❤️ by 🍌")

components.html(buy_a_coffee)