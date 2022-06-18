class BaseConnector(object):
    """
    Base class that should be inherited by all connectors
    """

    def __init__(self):
        pass

    def get_pandas_df(self, conn):
        raise NotImplementedError("This method needs to be overridden")

    def get_pandas_df(self, query, conn):
        raise NotImplementedError("This method needs to be overridden")
