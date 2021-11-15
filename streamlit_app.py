import mysql.connector
import pandas as pd
import streamlit as st

from streamlit_queries import (
    top_reporter,
    select_all,
    total_number_of_errands,
    created_errands_per_date,
    created_errands_per_type,
)
from streamlit_tools import (
    clean_dataframe,
    reformat_dataframe,
    add_info_flags,
    get_closed_stats_per_category,
    get_open_stats_per_category,
    transform_errands_per_date,
    transform_top_reporter_data,
    transform_errand_per_category,
    get_open_errands_details,
    convert_df_for_download,
)

st.set_page_config(
    page_title="Brf Tripolis ärenden", page_icon=":wrench:", layout="centered"
)


def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])


@st.cache()
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


conn = init_connection()
total_number_of_errands = run_query(total_number_of_errands)
select_all = run_query(select_all)
errands_per_date_raw_data = run_query(created_errands_per_date)
df_errands_per_date = transform_errands_per_date(errands_per_date_raw_data)
top_reporter_data = run_query(top_reporter)
errands_per_category_data = run_query(created_errands_per_type)


df_all = pd.DataFrame(select_all)
df_all_cleaned = clean_dataframe(df_all)
df_all_cleaned_reformatted = reformat_dataframe(df_all_cleaned)
df_all_cleaned_reformatted_with_flags = add_info_flags(df_all_cleaned_reformatted)

df_close_stats = get_closed_stats_per_category(df_all_cleaned_reformatted_with_flags)
df_open_stats = get_open_stats_per_category(df_all_cleaned_reformatted_with_flags)
df_top_reporter = transform_top_reporter_data(top_reporter_data)
df_errands_per_category = transform_errand_per_category(errands_per_category_data)
df_open_now_details = get_open_errands_details(df_all_cleaned_reformatted_with_flags)


st.title("Brf Tripolis")
password_to_view = st.text_input("Ange lösenord för att se dashboard", type="password")

if password_to_view == st.secrets["dashboard"]["password"]:
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Total antal ärenden", value=total_number_of_errands[0][0])

    with col2:
        st.metric(
            label="Antal öppna ärenden", value=int(df_open_stats["num errands"].sum())
        )

    st.subheader("Genomsnittligt antal dagar att stänga ett ärende per ärendetyp")
    col4, col5, col6, col7, col8 = st.columns(5)

    with col4:
        st.metric(
            label=f"{df_close_stats.loc[0][0]}", value=int(df_close_stats.iloc[0][1])
        )

    with col5:
        st.metric(
            label=f"{df_close_stats.iloc[1][0]}", value=int(df_close_stats.iloc[1][1])
        )

    with col6:
        st.metric(
            label=f"{df_close_stats.iloc[2][0]}", value=int(df_close_stats.iloc[2][1])
        )

    with col7:
        st.metric(
            label=f"{df_close_stats.iloc[3][0]}", value=int(df_close_stats.iloc[3][1])
        )

    with col8:
        st.metric(
            label=f"{df_close_stats.iloc[4][0]}", value=int(df_close_stats.iloc[4][1])
        )

    st.subheader("Antalet skapade ärenden")
    st.area_chart(df_errands_per_date)

    st.subheader("Antalet skapade ärenden per kategori")
    st.plotly_chart(df_errands_per_category)

    st.subheader("Antal skapade ärenden per medlem")
    st.dataframe(df_top_reporter)

    st.subheader("Öppna ärenden just nu")
    st.dataframe(df_open_now_details)
    st.download_button(
        "Ladda ner öppna ärenden",
        convert_df_for_download(df_open_now_details),
        file_name="oppna_arenden.csv",
        mime="text/csv",
    )
