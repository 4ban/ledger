import subprocess
import os
import platform
import re
import shutil
import requests
import json
import random
from time import sleep

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
         #self.producer = "http://api.kylin.alohaeos.com"
        self.producer = "http://127.0.0.1:8888"


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


 # EOS8HCdRC79RwDxdtus8rs7hpcz4gavgxqhKY7G7DZQLWbtJArziG
if __name__ == '__main__':
    account = Account()
    blockchain = BlockChain()
    account.name = 'tstvtxledger'
    # init 
    object = '["tstvtxledger", "vtxdistrib", "vtxtrust", 100, "", "EOS6EcERTUvtafcLMtrKycWF4JX5tFHnD7d9TPfyF1pdh6tgiWPpf", "test", "nonce"]'
    out = subprocess.check_output([os.environ['CLEOS'], '--url', blockchain.producer, 'push', 'action', account.name, 'rcrdtfr', object, '-p', 'tstvtxledger' + '@active'])
    print('************************************************************************************************************************************************************')
    out = subprocess.check_output([os.environ['CLEOS'], '--url', blockchain.producer, 'get', 'table', account.name, account.name, 'entry', '-l', '10000' ])
    print(out)
    
    print('************************************************************************************************************************************************************')
    #    object = '["tstvtxledger", "vtxdistrib", "vtxtrust", 10, "EOS8HCdRC79RwDxdtus8rs7hpcz4gavgxqhKY7G7DZQLWbtJArziG", "EOS6EcERTUvtafcLMtrKycWF4JX5tFHnD7d9TPfyF1pdh6tgiWPpf", "test","nonce"]'
    # cleos --url http://api.kylin.alohaeos.com push tstvtxledger rcrdtfr '["tstvtxledger", "vtxdistrib", "vtxtrust", 10,"EOS62L2r4FqnCbHAspPS3KBByGa728G3UDYxGkTY15mad97M4JhzN", "", "test", "nonce"]' -p tstvtxledger@active
#     print(str(out))
#     print('************************************************************************************************************************************************************')
#     print("                                                                                                                                                            ");  
#     print('get table')
#     out = subprocess.check_output([os.environ['CLEOS'],'--url', blockchain.producer, 'get', 'table', account.name, account.name, "entry"])
#     print(str(out))
#     print('************************************************************************************************************************************************************')
#     print('test')
#     
   # out = subprocess.check_output([os.environ['CLEOS'],'--url', blockchain.producer, 'push', 'action', account.name, 'test', '[]', '-p', 'tstvtxledger' + '@active'])
   # print(str(out))
