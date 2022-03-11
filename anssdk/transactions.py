from algosdk import encoding
from pyteal import compileTeal, Mode
from algosdk.future.transaction import LogicSig
from algosdk import logic
import base64
from pyteal import *
from anssdk import constants, dot_algo_name_record
from algosdk.future import transaction

class Transactions:

    def __init__(self, client):
        self.algod_client = client

    def compile_program(self, algod_client, source_code) :
        compile_response = algod_client.compile(source_code.decode('utf-8'))
        return base64.b64decode(compile_response['result'])            

    def prep_name_record_logic_sig(self, name, reg_app_id):
        reg_escrow_acct = logic.get_application_address(reg_app_id)
        logic_sig_teal = compileTeal(dot_algo_name_record.ValidateRecord(name,reg_app_id,reg_escrow_acct), Mode.Signature, version=4)
        validate_name_record_program = self.compile_program(self.algod_client, str.encode(logic_sig_teal))
        lsig = LogicSig(validate_name_record_program)
        return lsig 

    def get_name_price(self, name):
        assert(len(name)>=3 and len(name)<=64)
        # Returns name price in ALGOs
        if(len(name)==3):
            return 150000000
        elif(len(name)==4):
            return 50000000
        else:
            return 5000000        

    def prep_name_reg_gtxn(self,sender, name, validity):
        
        reg_app_id = constants.APP_ID
        algod_client = self.algod_client
        # Prepare group txn array
        Grp_txns_unsign = []

        # 1. PaymentTxn to Smart Contract
        reg_escrow_acct = logic.get_application_address(reg_app_id)
        pmnt_txn_unsign = transaction.PaymentTxn(sender, algod_client.suggested_params(), reg_escrow_acct, self.get_name_price(name), None)
        Grp_txns_unsign.append(pmnt_txn_unsign)


        # 2. Funding lsig
        lsig = self.prep_name_record_logic_sig(name, reg_app_id)
        # Min amount necessary: 915000
        fund_lsig_txn_unsign = transaction.PaymentTxn(sender, algod_client.suggested_params(), lsig.address(), 915000, None, None)
        Grp_txns_unsign.append(fund_lsig_txn_unsign)

        # 3. Optin to registry
        optin_txn_unsign = transaction.ApplicationOptInTxn(lsig.address(), algod_client.suggested_params(), reg_app_id)
        Grp_txns_unsign.append(optin_txn_unsign)

        # 4. Write name and owner's address in local storage
        txn_args = [
            "register_name".encode("utf-8"),
            name.encode("utf-8"),
            validity.to_bytes(8, "big")
        ]
        store_owners_add_txn_unsign = transaction.ApplicationNoOpTxn(sender, algod_client.suggested_params(), reg_app_id, txn_args, [lsig.address()])
        Grp_txns_unsign.append(store_owners_add_txn_unsign)

        gid = transaction.calculate_group_id(Grp_txns_unsign)
        for i in range(0,4):
            Grp_txns_unsign[i].group = gid

        return Grp_txns_unsign, lsig  

    def link_socials(self, domainname, platform_name, profile, sender):
        
        reg_app_id = constants.APP_ID
        algod_client = self.algod_client
        txn_args = [
            "update_name".encode("utf-8"),
            platform_name.encode("utf-8"),
            profile.encode("utf-8"),
        ]
        lsig = self.prep_name_record_logic_sig(domainname, reg_app_id)
        link_social_txn_unsign = transaction.ApplicationNoOpTxn(sender, algod_client.suggested_params(), reg_app_id, txn_args, [lsig.address()])        
        return link_social_txn_unsign

    def prep_renew_name_txn(self, domainname, years, sender):
        
        reg_app_id = constants.APP_ID
        algod_client = self.algod_client
        txn_args = [
            "renew_name".encode("utf-8"),
            years.to_bytes(8, "big")
        ]
        lsig = self.prep_name_record_logic_sig(domainname, reg_app_id)
        renew_name_txn = transaction.ApplicationNoOpTxn(sender, algod_client.suggested_params(), reg_app_id, txn_args, [lsig.address()])        
        return renew_name_txn        

    def init_name_tnsfr_txn(self, domainname, sender, tnsfr_price, recipient_addr):

        reg_app_id = constants.APP_ID
        algod_client = self.algod_client
        txn_args = [
            "initiate_transfer".encode("utf-8"),
            tnsfr_price.to_bytes(8, "big")
        ]
        lsig = self.prep_name_record_logic_sig(domainname, reg_app_id)
        txn_init_name_tnsfr_unsign = transaction.ApplicationNoOpTxn(sender, algod_client.suggested_params(), reg_app_id, txn_args, [lsig.address(),recipient_addr])
        return txn_init_name_tnsfr_unsign

    def prep_cmplte_name_tnsfr_gtxn(self, domainname, sender, tnsfr_price, recipient_addr):

        reg_app_id = constants.APP_ID
        algod_client = self.algod_client
        # Prepare group txn array   
        Grp_txns_unsign = []

        # 1. Payment for name transfer 
        pmnt_txn_unsign = transaction.PaymentTxn(sender, algod_client.suggested_params(), recipient_addr, tnsfr_price, None)
        Grp_txns_unsign.append(pmnt_txn_unsign)

        # 2. Transfer fee payment to registry 
        reg_escrow_acct = logic.get_application_address(reg_app_id)
        tnsfr_fee_pmnt_txn_unsign = transaction.PaymentTxn(sender, algod_client.suggested_params(), reg_escrow_acct, 2000000, None)
        Grp_txns_unsign.append(tnsfr_fee_pmnt_txn_unsign)

        # 3. 
        txn_args = [
            "accept_transfer".encode("utf-8"),
        ]
        lsig = self.prep_name_record_logic_sig(domainname, reg_app_id)
        txn_accpt_name_tnsfr_unsign = transaction.ApplicationNoOpTxn(sender, algod_client.suggested_params(), reg_app_id, txn_args, [lsig.address()])
        Grp_txns_unsign.append(txn_accpt_name_tnsfr_unsign)

        gid = transaction.calculate_group_id(Grp_txns_unsign)
        for i in range(3):
            Grp_txns_unsign[i].group = gid

        return Grp_txns_unsign        

        

                  