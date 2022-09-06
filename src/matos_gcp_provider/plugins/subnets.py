# -*- coding: utf-8 -*-
from typing import Any, Dict
from google.cloud import compute_v1
from matos_gcp_provider.lib import factory
from matos_gcp_provider.lib.base_provider import BaseProvider


class Subnet(BaseProvider):
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
        subnetworkClient = compute_v1.SubnetworksClient(credentials=self.credentials)
        networks = client.list(
            project=self.project_id
        )
        subnet_zones = []
        network_details = []
        for network in networks:
            for subnet in network.subnetworks:
                subnet_zones.append(subnet.split('/')[8])
        subnet_zones = [*set(subnet_zones)]#fetch only those region where subnet has created
        for region in subnet_zones:
            subnetworks = subnetworkClient.list(project=self.project_id, region=region)
            for subnet in subnetworks:
                # network_details[subnet.network] = final_networks[subnet.network]
                subnet_info = {
                        "name": subnet.name,
                        "enable_flow_logs": subnet.enable_flow_logs,
                        "ip_cidr_range": subnet.ip_cidr_range,
                        "network_name": subnet.network.split('/')[-1],
                        "private_ipv6_google_access": subnet.private_ipv6_google_access,
                        }
                network_details.append(subnet_info)
        return network_details


def register() -> Any:
    """Register plugins type"""
    factory.register("subnets", Subnet)
    