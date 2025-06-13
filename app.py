"""
Copyright (c) 2024-2025, All rights reserved, Use subject to license terms.
Scott Fehrman, scott.fehrman@sailpoint.com
"""

import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
from pyvis.network import Network
from typing import List
from utilities.charts import get_scatter, get_heatmap, get_scatter_3d, get_pie
from utilities.maps import get_pydeck_map
from utilities.graphs import get_reportsto
from utilities.sptk import sptk_service
from sailpoint.paginator import Paginator
from sailpoint.v2025.api.identities_api import IdentitiesApi
from sailpoint.v2025.models.identity import Identity

def main():
    st.set_page_config(page_title="Developer Days",page_icon="🚀",layout="wide")
    st.title("Developer Days 2025")

    identities_api: IdentitiesApi = sptk_service.get_identities_api()

    # --- Get all the identities ---

    identities: List[Identity] = Paginator.paginate(identities_api.list_identities, 10000)
    # st.header("Identities (objects)")
    # st.write(identities)

    # --- load into a dictionary (JSON) ---

    identities_dict = [identity.to_dict() for identity in identities]
    # st.header("Identities Dictionary (JSON)")
    # st.json(identities_dict)

    # --- Create a DataFrame ---

    df = pd.DataFrame(identities_dict)
    st.header("Identities DataFrame")
    st.dataframe(df)

    # --- Normalize the dictionary ---

    df_normalized = pd.json_normalize(identities_dict)
    st.header("Normalized Identities DataFrame")
    st.dataframe(df_normalized)
    # --- Location ---

    location_counts = df_normalized['attributes.location'].value_counts().reset_index()
    location_counts.columns = ['location', 'count']
    st.header("Location")
    st.bar_chart(location_counts.set_index('location'))
    st.plotly_chart(get_pie(location_counts, 'count', 'location'))

    # --- Department ---

    department_counts = df_normalized['attributes.department'].value_counts().reset_index()
    department_counts.columns = ['department', 'count']
    st.header("Department")
    st.bar_chart(department_counts.set_index('department')) 
    st.plotly_chart(get_pie(department_counts, 'count', 'department'))

    # --- Heatmap ---

    st.header("Department Distribution by Location")
    st.plotly_chart(get_heatmap(df_normalized,'attributes.department', 'attributes.location', 'count', 'Department', 'Location', 'Identities'))

    # --- Scatter Plot ---

    st.header("Department vs Location Scatter Plot")
    st.plotly_chart(get_scatter(df_normalized, 'attributes.department', 'attributes.location', 'count', 'Department', 'Location', 'Identities'))

    # --- 3D Scatter Plot ---

    st.header("3D Department-Location-Count Visualization")
    st.plotly_chart(get_scatter_3d(df_normalized, 'attributes.department', 'attributes.location', 'count', 'Department', 'Location', 'Identities'))

    # --- Map ---

    st.header("Map Locations and Counts")
    st.pydeck_chart(get_pydeck_map(identities=identities))

    # --- Graph ---

    st.header("Graph: Reports To")
    net: Network = get_reportsto(identities=identities)
    net.save_graph("identities_reportsto.html")
    with open("identities_reportsto.html", "r") as f:
        html_code = f.read()
    html(html_code, height=750)

if __name__ == "__main__":
    main()