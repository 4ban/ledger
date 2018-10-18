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
        #self.producer = "http://ec2-35-183-119-153.ca-central-1.compute.amazonaws.com:8888"
        self.producer = "http://api.kylin.alohaeos.com"
        #self.producer = "http://127.0.0.1"
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


class Wallet():
    def __init__(self):
        self.name = ""
        self.key = ""
        self.ownerPrivateKey = ''
        self.ownerPublicKey = ''
        self.activePrivateKey = ''
        self.activePublicKey = ''

    def erasePrivateKeys(self):
        self.ownerPrivateKey = ""
        self.activePrivateKey = ""


class Order():

    def __init__(self):
        self.to = ""
        self.amount = 0.0000
        self.contract = ""
        self.currency = ""
        self.contractAccountName = ""
        self.stakeCPU = ""
        self.stakeBandWidth = ""
        self.buyRam = 0

    def reset(self):
        self.to = ""
        self.amount = 0.0000
        self.contract = ""
        self.currency = ""
        self.contractAccountName = ""



def setContractSteps():
    out = ''
    try:
        out = subprocess.check_output([os.environ['CLEOS'], '--url', blockchain.producer, 'set', 'contract', account.name, order.contract, '-p', account.name])
    except:
        out = 'Cannot set contract steps'
    print(str(out))
    print('set contract steps')

def setupContract():
   
    compileContract()
    order.contract = os.environ['HOME'] + '/eclipse-workspace/ledger/stdvtxledger'
    setContractSteps()
    
def compileContract():
    out = subprocess.check_output(['/usr/local/eosio.cdt/bin/eosio-cpp', '-o', os.environ['HOME'] + '/eclipse-workspace/ledger/stdvtxledger/stdvtxledger.wasm' , os.environ['HOME'] + '/eclipse-workspace/ledger/stdvtxledger/stdvtxledger.cpp', '--abigen' ])
    out = subprocess.check_output(['/usr/local/eosio.cdt/bin/eosio-cpp', '-o', os.environ['HOME'] + '/eclipse-workspace/ledger/stdvtxledger/stdvtxledger.wast' , os.environ['HOME'] + '/eclipse-workspace/ledger/stdvtxledger/stdvtxledger.cpp' ])
    print(str(out))

if __name__ == '__main__':
    account = Account()
    order = Order()
    account.name = 'stdvtxledger'
    setupContract()
   

