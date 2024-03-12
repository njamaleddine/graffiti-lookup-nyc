import ssl
from urllib3.util.ssl_ import create_urllib3_context

from requests.adapters import HTTPAdapter


class LegacySslHttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        context = create_urllib3_context()
        context.load_default_certs()
        context.options = ssl.OP_LEGACY_SERVER_CONNECT
        pool_kwargs["ssl_context"] = context

        super().init_poolmanager(connections, maxsize, block, **pool_kwargs)
