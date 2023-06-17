class Connection:
    def __init__(
            self,
            conn_name,
            connector_name,
            conn_string,
            login="",
            pwd="",
            other_params=""
    ):
        self.conn_name = conn_name
        self.connector_name = connector_name
        self.conn_string = conn_string
        self.login = login
        self.pwd = pwd
        self.other_params = other_params

