# -*- coding: utf-8 -*-
from typing import Any, Dict
from google.cloud import storage as gcp_storage
from matos_gcp_provider.lib import factory
from matos_gcp_provider.lib.base_provider import BaseProvider


class storage(BaseProvider):
    """GCP cloud cloud storage class

    Args:
        BaseProvider (Class): Base provider class
    """

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct cloud storage service
        """
        self.resource = resource
        self.project_id = resource.pop("project_id")
        super().__init__(**kwargs)

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        client = gcp_storage.Client(credentials=self.credentials)

        # Initialize request argument(s)
        buckets = client.list_buckets(
            project=self.project_id
        )
        final_buckets = []
        for bucket in buckets:
            bucket_info = client.get_bucket(bucket.name)
            final_buckets.append({
                "id": bucket_info.id,
                "labels":  bucket_info.labels,
                "lifecycle_rules":  list(bucket_info.lifecycle_rules),
                "location":  bucket_info.location,
                "location_type":  bucket_info.location_type,
                "get_iam_policy":  [{"role": policy.get('role'), "members":list(policy.get('members'))} for policy in bucket_info.get_iam_policy().bindings],
                "get_logging":  bucket_info.get_logging(),
                "versioning_enabled": bucket_info.versioning_enabled,
                "retention_period": bucket_info.retention_period,
                "retention_policy_locked": bucket_info.retention_policy_locked,
                "default_kms_key_name": bucket_info.default_kms_key_name,
                "uniform_bucket_level_access_enabled": bucket_info.iam_configuration.uniform_bucket_level_access_enabled
            })
        return final_buckets

def register() -> Any:
    """Register plugins type"""
    factory.register("storage", storage)
