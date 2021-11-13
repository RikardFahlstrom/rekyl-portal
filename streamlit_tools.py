import datetime
import pandas as pd
import plotly.express as px
import streamlit as st


def clean_dataframe(df):
    df = df.drop(columns=[0])
    df.rename(
        columns={
            1: "errand_date",
            2: "scrape_time",
            3: "rekyl_id",
            4: "status",
            5: "reporter",
            6: "apartment",
            7: "kategori",
            8: "detaljer",
        },
        inplace=True,
    )

    return df


def reformat_dataframe(cleaned_df):
    reformat_df = (
        cleaned_df.groupby(["rekyl_id", "status", "kategori", "reporter", "detaljer"])
        .agg({"scrape_time": "min", "errand_date": "min"})
        .sort_values(by=["scrape_time"], ascending=False)
        .reset_index()
    )

    reformat_df["scrape_time"] = pd.to_datetime(reformat_df["scrape_time"])
    reformat_df["errand_date"] = pd.to_datetime(reformat_df["errand_date"])

    return reformat_df


def add_info_flags(reform_df):
    pivoted = reform_df.pivot(
        values=["scrape_time"],
        index=["rekyl_id", "errand_date", "kategori", "reporter", "detaljer"],
        columns=["status"],
    ).reset_index()

    pivoted["time_to_complete"] = (
        pivoted["scrape_time"]["Avslutad"] - pivoted["errand_date"]
    ).dt.days
    pivoted["is_completed"] = pivoted.apply(
        lambda row: "No" if pd.isnull(row.scrape_time.Avslutad) else "Yes", axis=1
    )

    start_date = datetime.datetime(2021, 9, 5)

    pivoted["after_start_scrape"] = start_date < pivoted["errand_date"]

    return pivoted


def get_closed_stats_per_category(df):
    df4 = df[(df["is_completed"] == "Yes") & (df["after_start_scrape"] == True)]
    df5 = df4[["rekyl_id", "kategori", "time_to_complete"]]
    df5.columns = df5.columns.droplevel(level=1)

    df5 = (
        df5.groupby(["kategori"])
        .agg({"time_to_complete": "mean", "rekyl_id": "count"})
        .rename(columns={"time_to_complete": "avg_days", "rekyl_id": "Antal ärenden"})
        .reset_index()
        .sort_values(by=["kategori"])
    )
    df5["avg_days"] = df5["avg_days"].astype("int")

    return df5


def get_open_stats_per_category(df):
    open_errands_df = df[df["is_completed"] == "No"]
    open_errands_df.columns = open_errands_df.columns.droplevel(level=1)

    return (
        open_errands_df.groupby(["kategori"])
        .agg({"rekyl_id": "count"})
        .rename(columns={"rekyl_id": "num errands"})
        .reset_index()
        .sort_values(by=["kategori"])
    )


def transform_errands_per_date(raw_data):
    df = pd.DataFrame(raw_data, columns=["Datum", "Antal ärenden"])
    df["Datum"] = pd.to_datetime(df["Datum"])
    df["datum_year_month"] = df["Datum"].apply(lambda x: x.strftime("%Y-%m"))

    return df.groupby(["datum_year_month"])["Antal ärenden"].sum()


def transform_top_reporter_data(raw_data):
    return pd.DataFrame(
        raw_data, columns=["Medlem", "Antal skapade ärenden", "Senaste ärende"]
    ).set_index(["Medlem"])


def transform_errand_per_category(raw_data):
    df = pd.DataFrame(raw_data, columns=["datum", "Kategori", "Antal ärenden"])
    df["datum"] = pd.to_datetime(df["datum"])
    df["Månad"] = df["datum"].apply(lambda x: x.strftime("%Y-%m"))
    df["kategori"] = df["Kategori"].astype("str")
    df["Antal ärenden"] = df["Antal ärenden"].astype("int")

    return px.line(
        df.groupby(["Månad", "Kategori"]).sum().fillna(0).reset_index(),
        x="Månad",
        y="Antal ärenden",
        color="Kategori",
        markers=True,
    )


def get_open_errands_details(df):
    df = df[df["is_completed"] == "No"]

    df = df[["rekyl_id", "errand_date", "kategori", "reporter", "detaljer"]]
    df.columns = df.columns.droplevel(level=1)
    df["errand_date"] = pd.to_datetime(df["errand_date"])
    df["errand_date"] = df["errand_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df.sort_values(by=["rekyl_id"], inplace=True)

    df = df.rename(
        columns={
            "rekyl_id": "Ärende ID",
            "errand_date": "Skapad",
            "kategori": "Kategori",
            "reporter": "Medlem",
            "detaljer": "Ärende",
        }
    )

    return df


@st.cache
def convert_df_for_download(df):
    return df.to_csv().encode("utf-8")
