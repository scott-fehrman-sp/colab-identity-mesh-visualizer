"""
Copyright (c) 2024-2025, All rights reserved, Use subject to license terms.
Scott Fehrman, scott.fehrman@sailpoint.com
SailPoint ToolKit: SPTK
"""

from typing import List
from sailpoint.configuration import Configuration
from sailpoint.v2025.api_client import ApiClient
from sailpoint.v2025.api.managed_clusters_api import ManagedClustersApi
from sailpoint.v2025.api.identities_api import IdentitiesApi
from sailpoint.v2025.models.managed_cluster import ManagedCluster

class SPTKService:
    """
    Manages the SailPoint ToolKit (SPTK) configuration and API client.
    
    This class provides a service for initializing and managing the SailPoint ToolKit
    configuration and API client. It handles the initialization of the configuration,
    the creation of the API client, and the validation of the API client.
    """
    config: Configuration
    api_client: ApiClient

    def __init__(self):
        """
        Initializes the SPTKService.
        
        This constructor initializes the configuration and API client for the SPTK service.
        It sets the experimental flag to True and creates an API client using the configuration.
        """
        self.__initialize()

    def __initialize(self) -> None:
        """
        Initializes the SPTKService.
        
        This method initializes the configuration and API client for the SPTK service.
        It sets the experimental flag to True and creates an API client using the configuration.
        """
        self.config = Configuration()
        self.config.experimental = True
        self.api_client = ApiClient(self.config)

    def __validate(self) -> None:
        """
        Validates the API client.
        
        This method validates the API client by attempting to retrieve managed clusters.
        If an exception occurs, it reinitializes the API client.
        """
        try:
            clusters: ManagedClustersApi = ManagedClustersApi(self.api_client)
            records: List[ManagedCluster] = clusters.get_managed_clusters()
        except Exception as e:
            print(f"... Error: {e} ... re-initializing ...")
            self.__initialize()
        
    def get_identities_api(self) -> IdentitiesApi:
        """
        Retrieves the Identities API.
        
        This method retrieves the Identities API by validating the API client and returning
        an instance of the IdentitiesApi class.
        """
        self.__validate()
        return IdentitiesApi(self.api_client)
    
try:
    sptk_service = SPTKService()
except ValueError as e:
    print(f"Warning: SailPoint configuration error: {str(e)}")
    sptk_service = None 