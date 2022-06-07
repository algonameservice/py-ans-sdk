from anssdk.resolver import AnsResolver
from anssdk.transactions import Transactions


class Address:
    def __init__(self, address, client, indexer):
        self.address = address
        self.resolver_obj = AnsResolver(client, indexer)

    def get_names(self, socials=False, metadata=False, limit=10):
        return self.resolver_obj.get_names_owned_by_address(self.address, socials, metadata, limit)
