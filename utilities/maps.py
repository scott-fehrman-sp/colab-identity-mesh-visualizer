"""
Copyright (c) 2024-2025, All rights reserved, Use subject to license terms.
Scott Fehrman, scott.fehrman@sailpoint.com
"""

import pydeck
import pandas as pd
from typing import Any, List, Dict
from utilities.coordinates import CoordinatesManager
from sailpoint.v2025.models.identity import Identity

def get_pydeck_map(identities: List[Identity]) -> pydeck.Deck:
    """
    Creates a pydeck map visualization of the identities.
    
    This function generates a pydeck map visualization of the identities,
    including a column layer for the locations and a view state for the map.
    """

    coordmgr: CoordinatesManager = CoordinatesManager()
    lat: float = 0.0
    lon: float = 0.0
    deck: pydeck.Deck
    identity: Identity
    attributes_dict: Dict[str, Any] = {}
    attr_location: str
    location_dict: Dict[str, dict] = {} # {location: {City: ABC, Qty: 0, Latitude: 0.0, Longitude: 0.0}}
    map_data: pd.DataFrame
    column_layer: pydeck.Layer
    view_state: pydeck.ViewState

    for identity in identities:
        if identity.attributes:
            attributes_dict = identity.attributes
            if attributes_dict.get("location"):
                attr_location = str(attributes_dict.get("location"))
                if attr_location:
                    if attr_location not in location_dict:
                        lat, lon = coordmgr.get(attr_location)
                        location_dict[attr_location] = {"City": attr_location, "Qty": 1, "Latitude": lat, "Longitude": lon}
                    else:
                        location_dict[attr_location]["Qty"] += 1
                else:
                    attr_location = "Unknown"
                    location_dict[attr_location] = {"City": attr_location, "Qty": 1, "Latitude": 0.0, "Longitude": 0.0}
        else:
            print(f"WARNING: Identity {identity.id} has no attributes.")

    map_data = pd.DataFrame(location_dict).T
    map_data["Radius"] = map_data["Qty"] * 1000
    map_data["Elevation"] = map_data["Qty"] * 1000

    column_layer = pydeck.Layer(
        "ColumnLayer",
        data=map_data,
        get_position=["Longitude", "Latitude"],
        get_elevation="Elevation",
        elevation_scale=50,
        radius=20000,
        get_fill_color=[102, 204, 0],
        auto_highlight=True,
        pickable=True,
    )

    view_state = pydeck.ViewState(
        latitude=30,
        longitude=-40,
        zoom=2,
        min_zoom=0,
        max_zoom=15,
        pitch=45,
        bearing=0,  # negative moves perspective to the right
    )

    deck = pydeck.Deck(
        column_layer,
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v9",
        tooltip={"text": "{Qty} employees in {City}"}, # type: ignore
    )

    return deck