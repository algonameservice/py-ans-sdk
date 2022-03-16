'''
Copyright (c) 2022 Algorand Name Service

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
'''


import unittest
import ans_helper as anshelper


import sys
sys.path.append('../')
from anssdk import constants, transactions

from anssdk.resolver import ans_resolver
#from anssdk import transactions

unittest.TestLoader.sortTestMethodsUsing = None

class TestDotAlgoNameRegistry(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.algod_client = anshelper.SetupClient()
        cls.algod_indexer = anshelper.SetupIndexer()
        cls.app_index = constants.APP_ID
        cls.resolver_obj = ans_resolver(cls.algod_client, cls.algod_indexer)
        #cls.transactions_obj = transactions.Transactions(cls.algod_client)


    def test_name_resolution(self):
        
        account_info = self.resolver_obj.resolve_name('rand')
        self.assertEqual(account_info["owner"], 'RANDGVRRYGVKI3WSDG6OGTZQ7MHDLIN5RYKJBABL46K5RQVHUFV3NY5DUE')

    '''
    def test_names_owned_by_address(self):
        
        account_info = self.resolver_obj.get_names_owned_by_address('RANDGVRRYGVKI3WSDG6OGTZQ7MHDLIN5RYKJBABL46K5RQVHUFV3NY5DUE')
        self.assertGreaterEqual(len(account_info), 2)
         

    def prep_name_reg_txns(self):
        
        name_reg_txns = self.transactions_obj.prep_name_reg_gtxn(
            'RANDGVRRYGVKI3WSDG6OGTZQ7MHDLIN5RYKJBABL46K5RQVHUFV3NY5DUE',
            'xyz01234',
            5
        )
        print(name_reg_txns)
    '''        


if __name__ == '__main__':
    unittest.main()
