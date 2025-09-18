import logging

class EndpointFilter(logging.Filter):
    endpoint: str

    def __init__(self, endpoint: str, *args, **kwargs):
        self.endpoint = endpoint
        super().__init__(*args, **kwargs)

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter for logging messages by endpoint.

        Args:
            record:
                Record of logging message.

        Returns:
            True if endpoint is not in message, False otherwise
        """

        return record.getMessage().find(self.endpoint) == -1
