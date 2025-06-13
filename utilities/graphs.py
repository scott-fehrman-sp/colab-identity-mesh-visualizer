"""
Copyright (c) 2024-2025, All rights reserved, Use subject to license terms.
Scott Fehrman, scott.fehrman@sailpoint.com
"""

import utilities.constants as CONSTANTS
from pyvis.network import Network
from typing import List, Dict, Any
from pydantic import StrictStr
from sailpoint.v2025.models.identity import Identity


def get_reportsto(identities: List[Identity]) -> Network:
    """
    Creates a network graph visualization of the reporting relationships between identities.
    
    This function builds a directed graph where each node represents an identity and edges
    represent reporting relationships. Managers are displayed as hexagons, while regular
    employees are displayed as dots. Node colors are based on location, and node sizes
    vary based on whether the identity is a manager.
    
    Args:
        identities (List[Identity]): A list of Identity objects to visualize in the graph
        
    Returns:
        Network: A pyvis Network object containing the reporting relationships graph
    """

    net: Network
    identity: Identity
    identity_dict: Dict[str, Identity] = {}
    identity_id: StrictStr
    identity_name: str
    manager_id: str
    attr_title: str
    attr_department: str
    attr_location: str
    attributes_dict: Dict[str, Any] # identity attributes
    node_label: str # node name
    node_title: str # node name
    node_color: str # color for the node
    node_size: int # size for the node
    node_shape: str # shapes: "dot", "diamond", "star", "triangle", "triangleDown", "square", "hexagon", "hexagonVertical", "text"
    location_colors: List[str] = [] # a list of colors for the locations
    location_dict: Dict[str, str] = {} # location -> color
    color_offset: int = 0

    net = Network(height="750px", width="100%", directed=True)

    location_colors = CONSTANTS.SPTK_WHITEBG_COLORS

    # Loop through the list of identities and add them to the graph as nodes
    for identity in identities:
        if identity.id:
            identity_id = identity.id
            identity_dict[identity_id] = identity

            identity_name = identity.name

            node_label = identity_name
            node_title = identity_name

            if identity.is_manager == True:
                node_size = 30
                node_shape = "hexagon"
            else:
                node_size = 20
                node_shape = "dot"

            attr_title = ""
            attr_department = ""
            attr_location = "Unknown"

            if identity.attributes:
                attributes_dict = identity.attributes

                if attributes_dict.get(CONSTANTS.TITLE):
                    attr_title = str(attributes_dict.get(CONSTANTS.TITLE))
                    if attr_title:
                        node_title += f"\n{attr_title}"

                if attributes_dict.get(CONSTANTS.DEPARTMENT):
                    attr_department = str(attributes_dict.get(CONSTANTS.DEPARTMENT))
                    if attr_department:
                        node_title += f"\nDepartment: {attr_department}"

                if attributes_dict.get(CONSTANTS.LOCATION):
                    attr_location = str(attributes_dict.get(CONSTANTS.LOCATION))
                    if attr_location:
                        node_title += f"\nLocation: {attr_location}"

                if attr_location not in location_dict:
                    location_dict[attr_location] = location_colors[color_offset]
                    color_offset += 1

                node_color = location_dict[attr_location] # each location has a different color

                net.add_node(identity_id, label=node_label, title=node_title, size=node_size, shape=node_shape, color=node_color)

                # print(f"Node: {identity_id} - {identity_name}") # DEBUG
            else:
                print(f"WARNING: Identity {identity_id} has no attributes") # DEBUG
                continue
        else:
            print(f"WARNING: Identity has no ID (unlikely)")
            continue

    # Iterate through the dictionary of identities and add edges between the identity and its manager
    for identity_id, identity in identity_dict.items():
        if identity.manager_ref and identity.manager_ref.id:
            manager_id = identity.manager_ref.id
            if manager_id in identity_dict:
                if manager_id == identity_id: # Self reference
                    edge_color = "red"
                else:
                    edge_color = "black"
                net.add_edge(identity_id, manager_id, color=edge_color)
                # print(f"Edge: {identity.get('name')} -> {identity.get('managerRef').get('name')}") # DEBUG
            else: # Manager reference does not exist, to add "unknown manager" node, uncomment the following lines
                # if "not_exist" not in identity_dict:
                #     net.add_node("not_exist", label="Not Found", color="black", size=30, shape="diamond")
                # net.add_edge(identity_id, "not_exist", color="red")
                continue
        else:
            continue # No manager reference, do nothing

    return net
