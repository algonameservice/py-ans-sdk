
from curses import meta
from anssdk.resolver import AnsResolver
from anssdk.transactions import Transactions
import datetime

class Name:
    def __init__(self, name, client, indexer=None):
        self.name=name
        self.resolver_obj = AnsResolver(client, indexer)
    
    def get_owner(self):
        domain_info = self.resolver_obj.resolve_name(self.name)
        if(domain_info['found'] is True):
            return domain_info['owner']

    def get_value(self):
        domain_info = self.resolver_obj.resolve_name(self.name)
        if(domain_info['found'] is True):
            return domain_info['value']

    def get_content(self):
        metadata = self.resolver_obj.resolve_name(self.name)['metadata']
        for data in metadata:
            if(data.get('content') is not None):
                return data.get('content')

    def get_text(self, key):
        metadata = self.resolver_obj.resolve_name(self.name)['metadata']
        socials = self.resolver_obj.resolve_name(self.name)['socials']
        for data in metadata:
            if(data.get(key) is not None):
                return data.get(key)    

        for data in socials:
            if(data.get(key) is not None):
                return data.get(key)    

        raise Exception('Property {key} is not set'.format(key = key))

    def get_all_information(self):
        return self.resolver_obj.resolve_name(self.name)

    def get_expiry(self):
        info = self.resolver_obj.resolve_name(self.name)
        if(info['found'] is True):
            return datetime.datetime.fromtimestamp(info['expiry'])
    