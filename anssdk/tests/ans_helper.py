'''
Copyright (c) 2022 Algorand Name Service

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
'''

from algosdk.v2client import algod, indexer
from pyteal import *

import sys
sys.path.append('../')
from anssdk import constants

from anssdk.dot_algo_name_record import ValidateRecord

import base64
import datetime,time

def SetupClient():
    
    # Purestake conn
    algod_address = "https://mainnet-api.algonode.cloud"
    
    algod_client=algod.AlgodClient("", algod_address)
    return algod_client

def SetupIndexer():
    

    algod_address = "https://mainnet-idx.algonode.cloud"
    
    algod_indexer=indexer.IndexerClient("", algod_address)
    
    return algod_indexer
