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
        final_networks = {}
        subnet_zones = []
        network_details = {}
        for network in networks:
            final_networks[network.self_link] = {
                "name": network.name,
                "self_link": network.self_link,
                "auto_create_subnetworks": network.auto_create_subnetworks,
                }
            for subnet in network.subnetworks:
                subnet_zones.append(subnet.split('/')[8])
        subnet_zones = [*set(subnet_zones)]
        for region in subnet_zones:
            subnetworks = subnetworkClient.list(project=self.project_id, region=region)
            for subnet in subnetworks:
                network_details[subnet.network] = final_networks[subnet.network]
                subnet_info = {
                        "name": subnet.name,
                        "enable_flow_logs": subnet.enable_flow_logs,
                        "ip_cidr_range": subnet.ip_cidr_range,
                        "private_ipv6_google_access": subnet.private_ipv6_google_access,
                        }
                if not network_details.get(subnet.network).get("subnets"):
                    network_details[subnet.network]["subnets"] = [subnet_info]
                else:
                      network_details[subnet.network]["subnets"].append(subnet_info)
        return [network_details.get(network) for network in network_details.keys()]


def register() -> Any:
    """Register plugins type"""
    factory.register("Subnet", Subnet)
    