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
        self.password =''

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
        
def setContractSteps():
    out = ''
    try:
        out = subprocess.check_output([os.environ['CLEOS'], '--url', blockchain.producer, 'set', 'code', account.name, '/mnt/c/Users/xuand/Documents/ledger/prevtxledger/prevtxledger.wasm'])
        out = subprocess.check_output([os.environ['CLEOS'], '--url', blockchain.producer, 'set', 'abi', account.name,  '/mnt/c/Users/xuand/Documents/ledger/prevtxledger/prevtxledger.abi'])
    except:
        out = 'Cannot set contract steps'
    print(str(out))
    print('set contract steps')


def setupContract():   
    compileContract()
    order.contract = '/mnt/c/Users/xuand/Documents/ledger/prevtxledger
    setContractSteps()

    
def compileContract():
    out = subprocess.check_output(['/usr/local/eosio.cdt/bin/eosio-cpp', '-o', '/mnt/c/Users/xuand/Documents/ledger/prevtxledger/prevtxledger.wasm' , '/mnt/c/Users/xuand/Documents/ledger/prevtxledger/prevtxledger.cpp', '--abigen' ])
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

def openWallet():
    print('open *************************************************************************************************', wallet.name, ':wallet')
    out = subprocess.check_output([os.environ['CLEOS'], 'wallet', 'open', '-n', wallet.name])
    print(out)
    
def unlockWallet():
    cwd = os.getcwd()
    path = cwd + '/prevtxledger'
    file = open(path, 'r') 
    pswd = file.read() 
    pswd = pswd[1:]
    pswd = pswd[:-1]
    print(pswd)
    print(wallet.name)
    print('unlock', wallet.name, ' : ', pswd)
    out = subprocess.check_output([os.environ['CLEOS'], 'wallet', 'unlock', '-n', wallet.name, '--password', pswd])
    
    print(out)
def lockWallet():
    print('open *************************************************************************************************', wallet.name, ':wallet')
    out = subprocess.check_output([os.environ['CLEOS'], 'wallet', 'lock', '-n', wallet.name])
    print(out)


if __name__ == '__main__':
    account = Account()
    order = Order()
    wallet = Wallet()
    blockchain = BlockChain()     
    wallet.name = 'prevtxledger'
    wallet.password = 'PW5JvkjBKhVbXmm72RumjquPG43PRiMjPKAmVBMSXRRRbsNh9pnwT'
    openWallet()
    unlockWallet()
    print('************************************************************************************************************************************************************')                                                                                                                            
    #account to wallet
    account.name = 'prevtxledger'
    object = '["prevtxledger", "vtxdistrib", "vtxtrust", 100, "", "EOS6EcERTUvtafcLMtrKycWF4JX5tFHnD7d9TPfyF1pdh6tgiWPpf", "test", "nonce"]'
    out = subprocess.check_output([os.environ['CLEOS'], '--url', blockchain.producer, 'push', 'action', account.name, 'rcrdtfr', object, '-p', 'prevtxledger' + '@active'])
    print('************************************************************************************************************************************************************')
    lockWallet()
    
    

