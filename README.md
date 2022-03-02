# PY-ANS-SDK

## Install package

```
pip3 install anssdk
```

### Import package
```
import anssdk.resolver as resolver

algod_client = "" # set up your algodV2 client
algod_indexer = "" # set up your algod indexer

#indexer and client must point to mainnet

resolver_obj = resolver.ans_resolver(client, indexer)
```

### Resolve .algo name

```
name = "ans.algo"

name_info = resolver_obj.resolver_name(name)

if(name_info["found"] is True):
    print(name_info["address"])
else:
    print('Name not registered')    
```

### Get names owned by an address

```
address="" # provide an algorand wallet address here

names = resolver_obj.get_names_owned_by_address(address)

if(len(names) > 0):
    for name in names:
        print(name)
else:
    print('No names registered by given address')        
```