[![Test](https://github.com/cloudmatos/matos-gcp-provider/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/cloudmatos/matos-gcp-provider/actions/workflows/test.yaml)
[![Pylint](https://github.com/cloudmatos/matos-gcp-provider/actions/workflows/pylint.yaml/badge.svg?branch=main)](https://github.com/cloudmatos/matos-gcp-provider/actions/workflows/pylint.yaml)


# matos-gcp-provider
The 'matos-gcp-provider' is an open-source python package for developing security tools to identify threats in your Google Cloud Platform (GCP) infrastructure. It uses the service providers Cloud SDK to deduce the current state and metadata of the underlying services.

### Quickstart
1. Clone this repository.
2. Create a virtualenv and activate.
3. Install requirement packages inside install_requires list of setup.py list.
4. Sample demo, import working folder into path ``src\matos_gcp_provider``
```python
from matos_gcp_provider.provider import Provider 
#credential can be import by either input dict or json load inside /credentials folder
dummy_credential = {
  "tenantId": "",
  "clientId": "",
  "clientSecret": "",
  "subscription_id": ""
}
# construct provider object, optional resource type for select specific resource
provider = Provider(dummy_credential=dummy_credential, resource_type="")
# asset discover 
assets = provider.get_assets()
# fetching resource details 
resources = provider.get_resource_inventories(assets)
```
5. Run prebuild package environment and unit test:
   ```sh
   python -m pip install -U tox
   python -m tox -e py
   ```
6. Build local wheel file
    ```sh
   python -m pip install -U setuptools wheel build
   python -m build .
   ```
   
### Add resource api plugin
- resource provider register through plugin design pattern, adding new plugin inside ``plugins`` folder
- Example resource and register step
```python

class SamplePlugin(BaseProvider):
    """service plugins

    Args:
        BaseProvider (Class): base provider class
    """
    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct cluster service
        """
        super().__init__(**kwargs)

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        pass
    
def register() -> Any:
    """Register plugins type"""
    factory.register("resource_type", SamplePlugin)
```
### Version handling and publish release
- Version is managed through bumpversion. Command to update new version, setup.py and .bumpversion.cfg will auto update
    ```sh
   bumpversion major|minor|patch --allow-dirty(optional)
   ``` 