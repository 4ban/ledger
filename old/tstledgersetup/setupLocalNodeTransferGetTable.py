import subprocess
import os
import platform
import re
import shutil
import requests
import json
import random
import psutil

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
        # self.producer = "http://api.kylin.alohaeos.com"
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


def setOwnerKeys():
    out = subprocess.check_output(["/usr/local/eosio/bin/cleos", "create", "key", "--to-console"])
    key = out[13:]
    key = key[:-67]
    key2 = out[77:]
    key2 = key2[:-1]
    wallet.ownerPrivateKey = key
    wallet.ownerPublicKey = key2
    print('Owner keys set')
    print(wallet.ownerPrivateKey)
        
        
def createEosioWallet():
    createWallet()
    setOwnerKeys()
    out = subprocess.check_output([os.environ['CLEOS'], 'wallet', 'import', '-n', 'eosio', '--private-key', '5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3'])
    out = subprocess.check_output([os.environ['CLEOS'], 'wallet', 'import', '-n', 'eosio', '--private-key', wallet.ownerPrivateKey])
    print(str(out))        

     
def createtstvtxledgerWallet():
    createWallet()
    out = subprocess.check_output([os.environ['CLEOS'], 'wallet', 'import', '-n', 'tstvtxledger', '--private-key', '5J9A3VhpRmkyqm1NmiTJW7MU34c7yVEF8Ep3rbSYR7r8hTHJrxD'])
    out = subprocess.check_output([os.environ['CLEOS'], 'wallet', 'import', '-n', 'tstvtxledger', '--private-key', '5KdakA6MZJeawKPECMgpG1Q2dffSt9BNSp5QwGbEKbeva7UaRAT'])
    print(str(out))        


def setContractSteps():
    out = ''
    try:
        #cleos --url http://api.kylin.alohaeos.com  set code eostitandocs eostitandocs.wasm
        #cleos --url http://api.kylin.alohaeos.com  set abi eostitandocs eostitandocs.abi

        out = subprocess.check_output([os.environ['CLEOS'], '--url', blockchain.producer, 'set', 'code', account.name,  os.environ['HOME'] + '/eclipse-workspace/ledger/tstvtxledger/tstvtxledger.wasm'])
        out = subprocess.check_output([os.environ['CLEOS'], '--url', blockchain.producer, 'set', 'abi', account.name,  os.environ['HOME'] + '/eclipse-workspace/ledger/tstvtxledger/tstvtxledger.abi'])
    except:
        out = 'Cannot set contract steps'
    print(str(out))
    print('set contract steps')


def setupContract():   
    compileContract()
    order.contract = os.environ['HOME'] + '/eclipse-workspace/ledger/tstvtxledger'
    setContractSteps()

    
def compileContract():
    out = subprocess.check_output(['/usr/local/eosio.cdt/bin/eosio-cpp', '-o', os.environ['HOME'] + '/eclipse-workspace/ledger/tstvtxledger/tstvtxledger.wasm' , os.environ['HOME'] + '/eclipse-workspace/ledger/tstvtxledger/tstvtxledger.cpp', '--abigen' ])
    out = subprocess.check_output(['/usr/local/eosio.cdt/bin/eosio-cpp', '-o', os.environ['HOME'] + '/eclipse-workspace/ledger/tstvtxledger/tstvtxledger.wast' , os.environ['HOME'] + '/eclipse-workspace/ledger/tstvtxledger/tstvtxledger.cpp' ])
    print(str(out))


def createAccount():
    print('creating *************************************************************************************************', account.name, ':account')
    out = ''
    out = subprocess.check_output([os.environ['CLEOS'], 'create', 'account', 'eosio', account.name, wallet.ownerPublicKey, wallet.activePublicKey, '-p', 'eosio'])
    print(str(out))


def createWallet():
    print('creating *************************************************************************************************', wallet.name, ':wallet')
    out = subprocess.check_output([os.environ['CLEOS'], 'wallet', 'create', '-n', wallet.name, '--to-console'])
    print(out)


def killKeosd():
    for p in psutil.process_iter(attrs=['pid', 'name']): 
        if 'keosd' in p.info['name']:
            pid = str(p.info['pid'])
            out = subprocess.check_output(['kill', pid])


if __name__ == '__main__':
    account = Account()
    order = Order()
    wallet = Wallet();
    blockchain = BlockChain()     
    killKeosd()
    out = subprocess.check_output(['rm', '-rf', os.environ['HOME'] + '/eosio-wallet/eosio.wallet'])
    print(out)
    wallet.name = 'eosio'
    createEosioWallet()
    out = subprocess.check_output(['rm', '-rf', os.environ['HOME'] + '/eosio-wallet/tstvtxledger.wallet'])
    print(out)
    wallet.name = 'tstvtxledger'
    createtstvtxledgerWallet()
    account.name = 'tstvtxledger'
    compileContract()
    createAccount()
    setupContract()
    print('************************************************************************************************************************************************************')  
    print('Wallet to Account')
    object = '["tstvtxledger", "vtxdistrib", "vtxtrust", 10,"EOS62L2r4FqnCbHAspPS3KBByGa728G3UDYxGkTY15mad97M4JhzN", "", "test", "nonce"]'
    out = subprocess.check_output([os.environ['CLEOS'],'--url', blockchain.producer, 'push', 'action', account.name, 'rcrdtfr', object, '-p', 'tstvtxledger' + '@active'])
    print('************************************************************************************************************************************************************')  
    print('Wallet to Account')
    out = subprocess.check_output([os.environ['CLEOS'],'--url', blockchain.producer, 'get', 'table', 'tstvtxledger', 'tstvtxledger', 'entry'])

