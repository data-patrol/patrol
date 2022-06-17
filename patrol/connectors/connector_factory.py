import sys
import json
import logging

log = logging.getLogger(__name__)

class ConnectorFactory:
    """
    Connector factory class
    """
    class ConnectorInfo:
        def __init__(self, module, class_name):
            self.module = module
            self.class_name = class_name

    def __init__(self):
        self._connectors = {}
        self.register_connectors()

    def register_connectors(self):
        # Register connectors from JSON file
        with open('../connectors/connectors.json') as json_file:
            data = json.load(json_file)
            for key in data:
                for subkey in data[key]:
                    connector_info = self.ConnectorInfo(subkey["connector.module"], subkey["connector.class"])
                    self._connectors[key] = connector_info
            
    def get_connector(self, connector_name):
        connector_module = self._connectors.get(connector_name).module
        connector_class_name = self._connectors.get(connector_name).class_name
        
        mod = __import__(connector_module, fromlist=[connector_class_name])
        connector = getattr(mod, connector_class_name)
        
        if not connector:
            raise ValueError(connector_name)
        return connector()
