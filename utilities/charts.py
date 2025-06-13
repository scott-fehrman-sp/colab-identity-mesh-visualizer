"""
Copyright (c) 2024-2025, All rights reserved, Use subject to license terms.
Scott Fehrman, scott.fehrman@sailpoint.com
"""

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

def get_pie(df: pd.DataFrame, values: str, names: str, hole: float = 0.3) -> Figure:
    """
    Creates a pie chart visualization of the data in the DataFrame.
    
    This function generates a pie chart using Plotly Express, which is a popular library
    for creating interactive and customizable charts in Python. The pie chart displays
    the proportion of each category in the DataFrame.
    """

    fig: Figure
    fig = px.pie(df, values=values, names=names, hole=hole)
    return fig

def get_heatmap(df: pd.DataFrame, x_attr: str, y_attr: str, data_attr: str, x_lbl: str, y_lbl: str, data_lbl: str) -> Figure:
    """
    Creates a heatmap visualization of the data in the DataFrame.
    
    This function generates a heatmap using Plotly Express, which is a popular library
    for creating interactive and customizable charts in Python. The heatmap displays
    the density of data points in a two-dimensional space defined by the x and y attributes.
    """

    fig: Figure
    heatmap_data: pd.DataFrame = df.groupby([x_attr, y_attr]).size().reset_index(name=data_attr)
    
    fig = px.density_heatmap(
        heatmap_data, 
        x=x_attr, 
        y=y_attr, 
        z=data_attr,
        labels={
            x_attr: x_lbl, 
            y_attr: y_lbl,
            data_attr: data_lbl
            },
        color_continuous_scale="Viridis"
    )
    return fig


def get_scatter(df: pd.DataFrame, x_attr: str, y_attr: str, data_attr: str, x_lbl: str, y_lbl: str, data_lbl: str) -> Figure:
    """
    Creates a scatter plot visualization of the data in the DataFrame.
    
    This function generates a scatter plot using Plotly Express, which is a popular library
    for creating interactive and customizable charts in Python. The scatter plot displays
    the relationship between two attributes in the DataFrame.
    """

    fig: Figure
    scatter_data: pd.DataFrame = df.groupby([x_attr, y_attr]).size().reset_index(name=data_attr)
    
    fig = px.scatter(
        scatter_data,
        x=x_attr,
        y=y_attr,
        size=data_attr,
        labels={
            x_attr: x_lbl,
            y_attr: y_lbl,
            data_attr: data_lbl
        },
        color=data_attr,
        color_continuous_scale='Viridis',
        hover_data=[data_attr]
    )
    return fig

def get_scatter_3d(df: pd.DataFrame, x_attr: str, y_attr: str, data_attr: str, x_lbl: str, y_lbl: str, data_lbl: str) -> Figure:
    """
    Creates a 3D scatter plot visualization of the data in the DataFrame.
    
    This function generates a 3D scatter plot using Plotly Express, which is a popular library
    for creating interactive and customizable charts in Python. The 3D scatter plot displays
    the relationship between three attributes in the DataFrame.
    """
    
    fig: Figure

    scatter_3d_data: pd.DataFrame = df.groupby([x_attr, y_attr]).size().reset_index(name=data_attr)
    
    fig = px.scatter_3d(
        scatter_3d_data,
        x=x_attr,
        y=y_attr,
        z=data_attr,
        color=data_attr,
        labels={
            x_attr: x_lbl,
            y_attr: y_lbl,
            data_attr: data_lbl
        },
        # title='3D View of Department, Location, and Identity Count',
        color_continuous_scale='Viridis',
        # opacity=0.7,
        hover_data=[data_attr]
    )

    return fig
