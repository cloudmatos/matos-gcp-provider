# -*- coding: utf-8 -*-
from typing import Any, Dict
from google.cloud import compute_v1
from google.protobuf.json_format import MessageToDict
from matos_gcp_provider.lib import factory
from matos_gcp_provider.lib.base_provider import BaseProvider


class VPC(BaseProvider):
    """GCP VPC class

    Args:
        BaseProvider (Class): Base provider class
    """

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct VPC service
        """
        self.resource = resource
        self.project_id = resource.pop("project_id")
        super().__init__(**kwargs)

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        client = compute_v1.NetworksClient(credentials=self.credentials)
        networks = client.list(
            project=self.project_id
        )
        final_networks = []
        for network in networks:
            final_networks.append(MessageToDict(network._pb))# pylint: disable=W0212
        return final_networks

def register() -> Any:
    """Register plugins type"""
    factory.register("VPC", VPC)
    