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
        #self.producer = "http://ec2-35-182-243-31.ca-central-1.compute.amazonaws.comi:8888"
        #self.producerWallets = "http://ec2-35-182-243-31.ca-central-1.compute.amazonaws.com:8900"
        #self.producer = "http://ec2-35-183-119-153.ca-central-1.compute.amazonaws.com:8888"
        self.producer = "http://api.kylin.alohaeos.com"
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
    wallet.ownerPrivateKey = '55J9A3VhpRmkyqm1NmiTJW7MU34c7yVEF8Ep3rbSYR7r8hTHJrxD'
    wallet.ownerPublicKey = 'EOS7zbDvgfqEuXmrXFz7dnhEC4w89w2vWq187p5shsne5rzjLs2VE'
    print('Owner keys set')
    print(wallet.ownerPrivateKey)


def setActiveKeys():
    out = subprocess.check_output(["/usr/local/eosio/bin/cleos", "create", "key", "--to-console"])
    key = out[13:]
    key = key[:-67]
    key2 = out[77:]
    key2 = key2[:-1]
    wallet.activePrivateKey = '5KdakA6MZJeawKPECMgpG1Q2dffSt9BNSp5QwGbEKbeva7UaRAT'
    wallet.activePublicKey = 'EOS8FhYPgnTXoSot5a16CxhcCSmaepvEY93D9WYgb16tB5QxAhDcc'
    print('Active keys set')
    print(wallet.activePrivateKey)


def importKeys():
    out = subprocess.check_output(
        ['/usr/local/eosio/bin/cleos', 'wallet', 'import', '-n', wallet.name, '--private-key', wallet.ownerPrivateKey])
    out1 = subprocess.check_output(
        ['/usr/local/eosio/bin/cleos', 'wallet', 'import', '-n', wallet.name, '--private-key', wallet.activePrivateKey])
    wallet.erasePrivateKeys()
    print('Keys imported to wallet')


def createWallet(name):
    walletDirectory = os.environ['HOME'] + '/eosio-wallet'
    if not os.path.exists(walletDirectory):
        os.makedirs(walletDirectory)
    out = subprocess.check_output(['/usr/local/eosio/bin/cleos', 'wallet', 'create', '-n', name, '--file', name])
    print(str(out))
	



    
if __name__ == '__main__':
    account = Account()
    wallet = Wallet()
    blockchain = BlockChain()
    order = Order()
    out = subprocess.check_output(['/usr/local/eosio/bin/cleos', 'wallet', 'open', '-n', 'prevtxledger'])
    out = subprocess.check_output(['/usr/local/eosio/bin/cleos', 'wallet', 'unlock', '-n', 'prevtxledger', '--password', 'PW5KRzmqfd9E1wK7RUqKULjjq7cU5aaeog3aexoRRWT5yym27GjYp'])
    print(str(out))
    #createWallet("prevtxledger")
    
    
