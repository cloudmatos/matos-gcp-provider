# -*- coding: utf-8 -*-
from typing import Any, Dict
from google.cloud import compute_v1
from google.protobuf.json_format import MessageToDict
from matos_gcp_provider.lib import factory
from matos_gcp_provider.lib.base_provider import BaseProvider

class Firewall(BaseProvider):
    """GCP VPC class

    Args:
        BaseProvider (Class): Base provider class
    """

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct VPC service
        """
        self.resource = resource
        self.resource_type = "instance"
        self.project_id = resource.pop("project_id")
        super().__init__(**kwargs)

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        firewallClient = compute_v1.FirewallsClient(credentials=self.credentials)
        firewallRules = firewallClient.list(project=self.project_id)
        finalFirewallRules = []
        for firewall in firewallRules:
            finalFirewallRules.append(MessageToDict(firewall._pb))# pylint: disable=W0212
        return finalFirewallRules
        

def register() -> Any:
    """Register plugins type"""
    factory.register("firewall", Firewall)
    