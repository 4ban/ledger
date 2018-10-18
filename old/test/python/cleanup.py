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
        self.producer = "http://ec2-35-183-119-153.ca-central-1.compute.amazonaws.com:8888"

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


def setActiveKeys():
    out = subprocess.check_output(["/usr/local/eosio/bin/cleos", "create", "key", "--to-console"])
    key = out[13:]
    key = key[:-67]
    key2 = out[77:]
    key2 = key2[:-1]
    wallet.activePrivateKey = '5KfpCFGR8SBZ3At7oGTDcHgzXgCZRGV6hCT7DTfReYQ63gi3gQz'
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
	


def setContractSteps():
    out = ''
    try:
        out = subprocess.check_output(
            [os.environ['CLEOS'], '--url', blockchain.producer, 'set', 'contract', account.name, order.contract, '-p',
             account.name])

    except:
        out = 'Cannot set contract steps'
    print(str(out))
    print('set contract steps')

def setupContract():
    out = subprocess.check_output(['rm', '-rf', os.environ['NODEOS_DATA']])
    flushWallets()
    createEosioWallet()
    wallet.name = 'vtxledger'
    createWallet('vtxledger')
    setActiveKeys()
    setOwnerKeys()
    importKeys()
    #account.name = 'vtxledger'
    #createAccount()
    compileContract()
    order.contract = os.environ['HOME'] + '/eclipse-workspace/ledger/vtxledger/'
    setContractSteps()


def rcrdtrf():
    object = '["vtxledger","vtxdistrib1","vtxdistrib",10000000, "", ""]'
    out = subprocess.check_output([os.environ['CLEOS'],'--url', blockchain.producer, 'push', 'action', account.name, 'rcrdtfr', object, '-p', 'vtxledger' + '@active'])
    print(str(out))


def getrcrd():
    out = subprocess.check_output([os.environ['CLEOS'], '--url', blockchain.producer, 'push', 'action', account.name, 'getrcrd', '[1234]', '-p', 'vtxledger' + '@active'])
    print(str(out))


def vtxledgerNullFromKey():
    object = '["vtxledger","distribution","trust","", "EOS62L2r4FqnCbHAspPS3KBByGa728G3UDYxGkTY15mad97M4JhzN", 50]'
    out = subprocess.check_output(
        [os.environ['CLEOS'], 'push', 'action', account.name, 'rcrdtfr', object, '-p', account.name + '@active'])
    print(str(out))


def vtxledgerMultipleEntries():
    object = '["vtxledger","distribution","trust","", "EOS62L2r4FqnCbHAspPS3KBByGa728G3UDYxGkTY15mad97M4JhzN", 50]'
    object2 = '["vtxledger","distribution","trust","", "EOS62L2r4FqnCbHAspPS3KBByGa728G3UDYxGkTY15mad97M4JhzN", 51]'
    out = subprocess.check_output(
        [os.environ['CLEOS'], 'push', 'action', account.name, 'rcrdtfr', object, '-p', account.name + '@active'])
    print(str(out))
    out = subprocess.check_output(
        [os.environ['CLEOS'], 'push', 'action', account.name, 'rcrdtfr', object2, '-p', account.name + '@active'])
    print(str(out))


def createEosioWallet():
    out = ''
    try:
        wallet.name = 'eosio'
        createWallet('eosio')
        setOwnerKeys()
        setActiveKeys()
        out = subprocess.check_output([os.environ['CLEOS'], 'wallet', 'import', '-n', 'eosio', '--private-key', '5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3'])
    except:
        out = 'could not create wallet'
    print(str(out))


def check_kill_process(pstring):
    for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
        fields = line.split()
        pid = fields[0]
    if pid > 0:
        os.kill(int(pid), signal.SIGKILL)


def flushWallets():
    rand = random.randint(1, 1000000)
    try:
        subprocess.check_output(
            ['mv', os.environ['HOME'] + '/eosio-wallet/', os.environ['HOME'] + '/eosio-wallet.save' + str(rand)])
        # check_kill_process(os.environ['EOS_KEOSD'])
    except:
        print('Could not move')




def createAccount():
    out = ''
    try:
        out = subprocess.check_output([os.environ['CLEOS'], '--url', blockchain.producer, 'create', 'account', 'eosio', account.name, wallet.ownerPublicKey, wallet.activePublicKey, '-p', 'eosio'])
    except:
        out = 'Could not create account'
    print(str(out))

def unlockWallets():
    try:	
    	out = subprocess.check_output(['/usr/local/eosio/bin/cleos', 'wallet', 'unlock', '-n', 'eosio', '--password', 'PW5JHYpoBnmhqng1ixyV1wz6a4Tu8mCUvwAdRyVE1otGupSRDWzBY'])
    	out = subprocess.check_output(['/usr/local/eosio/bin/cleos', 'wallet', 'unlock', '-n', 'vtxledger', '--password', 'PW5JUTVUM8XyvC4dVPhhyJtb23yMneWJQpQ3n9F4uUk8HV2uFyL3T'])
    except:
    	out = "could not unlock wallet"
    print("wallets already unlocked")	
	
def compileContract():
   
    out = subprocess.check_output(['/usr/local/eosio/bin/eosiocpp', '-o', os.environ['HOME'] + '/eclipse-workspace/ledger/vtxledger/vtxledger.wasm' , os.environ['HOME'] + '/eclipse-workspace/ledger/vtxledger/vtxledger.cpp' ])
    out = subprocess.check_output(['/usr/local/eosio/bin/eosiocpp', '-o', os.environ['HOME'] + '/eclipse-workspace/ledger/vtxledger/vtxledger.wast' , os.environ['HOME'] + '/eclipse-workspace/ledger/vtxledger/vtxledger.cpp' ])
    out = subprocess.check_output(['/usr/local/eosio/bin/eosiocpp', '-g', os.environ['HOME'] + '/eclipse-workspace/ledger/vtxledger/vtxledger.abi' , os.environ['HOME'] + '/eclipse-workspace/ledger/vtxledger/vtxledger.cpp' ])

if __name__ == '__main__':
    account = Account()
    wallet = Wallet()
    blockchain = BlockChain()
    order = Order()
    account.name = 'vtxledger'
    setupContract()
    #unlockWallets()
    #rcrdtrf()
    # vtxledgerNullFromKey()
    # vtxledgerMultipleEntries()
    #getrcrd()

