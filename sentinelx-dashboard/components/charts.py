# sentinelx-dashboard/components/charts.py

import plotly.express as px
import pandas as pd


def severity_chart(df, column="severity"):
    """
    Create a severity distribution chart.
    """

    if df.empty or column not in df.columns:
        return None

    counts = (
        df[column]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .reset_index()
    )

    counts.columns = ["severity", "count"]

    fig = px.bar(
        counts,
        x="severity",
        y="count",
        title="Findings by Severity",
        labels={
            "severity": "Severity",
            "count": "Number of Findings"
        }
    )

    return fig


def category_chart(df, column="type"):
    """
    Create a category distribution chart.
    """

    if df.empty or column not in df.columns:
        return None

    counts = (
        df[column]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .reset_index()
    )

    counts.columns = ["category", "count"]

    fig = px.pie(
        counts,
        names="category",
        values="count",
        title="Findings by Category"
    )

    return fig


def horizontal_bar_chart(
    df,
    category_column,
    value_column,
    title
):
    """
    Generic horizontal bar chart.
    """

    if df.empty:
        return None

    fig = px.bar(
        df,
        x=value_column,
        y=category_column,
        orientation="h",
        title=title
    )

    return fig