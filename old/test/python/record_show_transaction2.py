import subprocess
import os
import platform
import re
import shutil
import requests
import json
import random

home = os.environ['HOME']
os.environ['EOS_SOURCE'] = home + "/eos"
if platform.system() == 'Darwin':
    os.environ['NODEOS_DATA'] = home + "/Library/Application\ Support/eosio/nodeos/data"
elif platform.system() == 'Linux':
    os.environ['NODEOS_DATA'] = home + "/.local/share/eosio/nodeos/data/"
os.environ['EOS_NODEOS'] = "/usr/local/eosio/bin/nodeos"
os.environ['EOS_KEOSD'] = "/usr/local/eosio/bin/keosd"
os.environ['CLEOS'] = "/usr/local/eosio/bin/cleos"


class BlockChain():
    def __init__(self):
        self.producer = "http://api.kylin.alohaeos.com"
        #self.producer = "http://127.0.0.1:8888"
class Account():
    def __init__(self):
        self.name = ""
        self.creator = ""
        self.receiver = ""
        self.creatorOwnerKey = ""
        self.creatorActiveKey = ""
        self.cpu = ""
        self.bandwidth = ""
        self.ram = ""

if __name__ == '__main__':
    account = Account()
    blockchain = BlockChain()
    account.name = 'stdvtxledger'
    print('************************************************************************************************************************************************************')
    print("                                                                                                                                                            ");  
    print('Account to Wallet')
    object = '["stdvtxledger", "vtxdistrib", "vtxtrust", 123456,"", "EOS62L2r4FqnCbHAspPS3KBByGa728G3UDYxGkTY15mad97M4JhzN", "test", "nonce"]'
    out = subprocess.check_output([os.environ['CLEOS'],'--url', blockchain.producer, 'push', 'action', account.name, 'rcrdtfr', object, '-p', 'stdvtxledger' + '@active'])
    print(str(out))
    print('************************************************************************************************************************************************************')
    print("                                                                                                                                                            ");  
    print('get table')
    out = subprocess.check_output([os.environ['CLEOS'],'--url', blockchain.producer, 'get', 'table', account.name, account.name, "entry"])
    print(str(out))
    print('************************************************************************************************************************************************************')
    print('test')
    
   # out = subprocess.check_output([os.environ['CLEOS'],'--url', blockchain.producer, 'push', 'action', account.name, 'test', '[]', '-p', 'stdvtxledger' + '@active'])
   # print(str(out))
