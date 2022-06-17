class Connection:
    def __init__(
            self,
            connection_name,
            connection_string,
            connector_name,
            optional_params = ""
            ):
        self.connection_name = connection_name
        self.connection_string = connection_string
        self.connector_name = connector_name
        self.optional_params = optional_params