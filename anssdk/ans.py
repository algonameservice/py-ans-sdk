import algosdk
from anssdk.name import Name
from anssdk.address import Address
from anssdk.helper.validation import is_valid_name

class ANS:
    def __init__(self, client, indexer=None):
        if(indexer):
            self.indexer=indexer
        self.client=client
    
    def name(self, name):
        name = name.split('.algo')[0]
        if(is_valid_name(name)):
            return Name(name, self.client)
    
