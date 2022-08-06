# PY-ANS-SDK
A python sdk to resolve .algo names and perform name operations on ANS .algo names.

## Documentation


Install Package

**`pip`**
```
pip3 install anssdk
```

## Import
```
from anssdk.ans import ANS
```

## Setup

```
algod_client = "" # set up your algodV2 client
algod_indexer = "" # set up your algod indexer

#indexer is not required if the intention is to only resolve .algo names, but it is required to view the names owned by an algorand wallet address
#indexer and client must point to mainnet

sdk = ANS(algod_client, algod_indexer)
```


## Resolve .algo name
Resolve .algo name to get the address of the owner. The owner of the account is authorized to manage the domain including setting properties and transfer
```
name = "ans.algo"

owner = sdk.name(name).get_owner()
print(owner)
```

## Get value property
The value property is set by the owner to return a different address when resolving the domain names.
```
name = "ans.algo"

value_property = sdk.name(name).get_value()
print(value_property)
```

## Get content property
The content property is set by the user to host a website on web3 infrastructure. This is expected to be either a Skylink content ID or an IPFS content ID
```
name = "ans.algo"

content = sdk.name(name).get_content()
print(content)
```

## Get text record
Return text record (socials, avatar etc) set by the owner.
```
name = "ans.algo"
key = "discord"
record = sdk.name(name).get_text(key)
print(record)
```

## Get domain information
Return the entire domain information for the given domains.
```
name = "ans.algo"
information = sdk.name(name).get_all_information()
print(information)
```

## Register a new name


Prepare name registration transactions
```
name_to_register = "" #.algo name to register
address = "" # owner's algorand wallet address
period = 0 # duration of registration

try:

    name_registration_txns = sdk.name(name_to_register).register(address, period)

    # Returns a tuple of size two
    # name_registration_txns[0] includes the array of transactions
    # name_registration_txns[1] has the logic sig

    if(len(name_registration_txns[0]) == 2):

        # Lsig account previous opted in (name expired)
        # Sign both transactions
        # Send all to network

    elif(len(name_registration_txns[0]) == 4):

        # name_registration_txns[2] must be signed by the sdk
        # Sign name_registration_txns index 0,1,3
        # Submit transactions as a group

        signed_group_txns = []

        txns = [
            signed_group_txns[0],
            signed_group_txns[1],
            signed_group_txns[2], # must be signed by the sdk
            signed_group_txns[3]
        ]

        # send to network

except:
    pass
```

## Update Name (Set name properties)
This method returns transactions to set the social media handles of a domain name

```
try:

    name = "" #.algo name
    address = "" # owner's algorand address

    edited_handles = {
        'discord': '',
        'github': ''
    }

    update_name_property_txns = sdk.name(name).update(address, edited_handles)

    # Returns an array of transactions
    # Sign each and send to network

except:
    pass
```

## Renew Name
Retrieve transactions to renew a name. The ANS registry currently supports renewal only by the owner hence the transactions will fail if the input address is not the current owner of the name.

```
try:

    name = "" # .algo name
    owner = "" # owner address
    period = 0 # period for renewal

    name_renewal_txns =  sdk.name(name).renew(owner, period)

    # Returns an array of transactions 
    # Sign each and send to network

except:
    pass
```

## Update value
Value property is set by the owner of a domain if they wish to have their domain resolved to a different account.
Only the owner address can authorize any transactions on their domain

Get the transactions to update the value property associated with a .algo name

```
try:

    name = "" # .algo name
    owner = "" # owner address
    value = "" # value property as defined above

    name_renewal_txns =  sdk.name(name).set_value(owner, value)

    # Returns a transaction 
    # Sign and send to network

except:
    pass
```

## Set default account
Default domain, if set by the user, will be displayed instead of wallet addresses in ANS and services that have integrated ANS.

Get the transactions to update the default domain associated with a .algo name

```
try:

    name = "" # .algo name
    owner = "" # owner address
    
    name_renewal_txns =  sdk.name(name).set_default_domain(owner)

    # Returns a transaction 
    # Sign and send to network

except:
    pass
```

## Delete property
Properties set by the domain owner (socials and hosting information) can be deleted by the owner

Get the transactions to delete a property associated with a .algo name
```
try:

    name = "" # .algo name
    owner = "" # owner address
    property = "" # property as defined above

    name_renewal_txns =  sdk.name(name).delete_property(owner, property)

    # Returns a transaction 
    # Sign and send to network

except:
    pass
```

## Initiate transfer
This method returns a transaction to initiate name transfer. The owner is required to set the price for transfer and the recipient's algorand account address.

```
try:
    
    name = "" # .algo name to initiate transfer
    owner = "" # current owner
    new_owner = "" # new owner's address
    price = 0 # price at which the seller is willing to sell the name

    name_transfer_transaction = sdk.name(name).init_transfer( owner, new_owner, price)

    # Returns a transaction to be signed by `owner` 
    # Sign and send to network

except:
    pass
```

## Accept transfer
Retrieve the transactions to complete the transfer by providing the current owner's address, the transfer recipient's address, and the price set by the owner
```
try:
    
    name = "" # .algo name to accept transfer
    owner = "" # current owner
    new_owner = "" # new owner's address
    price = 0 # price set in the previous transaction

    accept_name_transfer_txns = sdk.name(name).accept_transfer( new_owner, owner, price)

    # Returns an array of transactions to be signed by `newOwner`
    # Sign each and send to network

except:
    pass
```

## Get domains owned by an address
Returns domains owned by an algorand address
```
address="" # provide an algorand address here
socials=True # return socials along with domain information
metadata=True # return metadata along with domain information
limit=1 #limit the number of domains to retrieve

domains = sdk.address(address).get_names(socials, metadata, limit)
print(domains)
```

## Get default domain
If configured, this method returns the default domain set by an address. If not configured, this method returns the most recently purchased domain by an address
```
address="" # provide an algorand address here

default_domain = sdk.address(address).get_default_domain()
print(default_domain)
```




