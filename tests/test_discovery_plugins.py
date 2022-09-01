import unittest
from matos_gcp_provider.provider import Provider

DUMMY_CREDS = {
    "type": "service_account",
    "project_id": "",
    "private_key_id": "",
    "private_key": "",
    "client_email": "",
    "client_id": "",
    "auth_uri": "https://XXX.XXX.com/o/oauth2/auth",
    "token_uri": "https://oauth2.XXX.com/token",
    "auth_provider_x509_cert_url": "https://www.XXX.com/XXX/v1/XX",
    "client_x509_cert_url": "https://www.XXXX.com/robot/v1/metadata/x509/XXX%XX-XXX.iam.XXXX.com"
}


class TestDiscoveryPlugin(unittest.TestCase):
    """Test Discovery plugin class"""
    def setUp(self):
        """set up plugin data for test"""
        self.service_type_map = {
            "cluster": "cluster",
            "instance": "instance",
        }

    def test_check_plugins_type_pass(self):
        """Test correct plugin type"""
        provider = Provider(credentials=DUMMY_CREDS)
        for key_type, resource_type in self.service_type_map.items():
            discovery_service = provider.service_factory.create(
                {"type": key_type, "project_id": "project_id", "credentials": DUMMY_CREDS}
            )
            self.assertEqual(discovery_service.resource_type, resource_type)


if __name__ == "__main__":
    unittest.main()
