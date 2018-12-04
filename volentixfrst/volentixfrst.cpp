#include <eosiolib/eosio.hpp>
#include <eosiolib/multi_index.hpp>
#include <string>
#include <eosiolib/transaction.hpp>
#include <eosiolib/time.hpp>

using namespace eosio;
using namespace std;

CONTRACT Ledger: public contract {
  public:
    using contract::contract;

    /*
    For the applying actions we need:
    receiver - is the account that is currently processing the action.
    code     - is the account that authorized the contract.
    action   - is the ID of the currently running action.
    */
    Ledger(name receiver, name code,  datastream<const char*> ds): contract(receiver, code, ds), ledger(receiver, receiver.value) {}

    ACTION rcrdtfr(name signer,
                  string fromaccount,
                  string toaccount,
                  double amount,
                  string tokey,
                  string comment,
                  string nonce) {

      // ledgertable ledger(_code, _code.value);

      double negAmount = -1 * amount;
      double posAmount = amount;

      uint64_t tbn = tapos_block_num();
      uint64_t tbp = tapos_block_prefix();
      uint64_t timestamp = current_time();

      ledger.emplace(get_self(), [&](auto& p)
      {
        p.key = ledger.available_primary_key();
        p.Id = ledger.available_primary_key();
        p.fromAccount = fromaccount;
        p.toAccount = "";
        p.sToKey = "";
        p.amount = negAmount;
        p.comment = comment;
        p.nonce = nonce;
        p.tbn = tbn;
        p.tbp = tbp;
        p.timestamp = timestamp;
      });
      //increase with tokey
      ledger.emplace(get_self(), [&](auto& p)
      {
        p.key = ledger.available_primary_key();
        p.Id = ledger.available_primary_key();
        p.fromAccount = "";
        p.toAccount = toaccount;
        p.sToKey = tokey;
        p.amount = posAmount;
        p.comment = comment;
        p.nonce = nonce;
        p.tbn = tbn;
        p.tbp = tbp;
        p.timestamp = timestamp;
      });

    }

  private:

    TABLE entry {
        name signer;
        uint64_t key = 0;
        uint64_t Id = 0;
        string sToKey;
        string fromAccount;
        string toAccount;
        double amount;
        string comment;
        string nonce;
        int64_t tbn;
        int64_t tbp;
        uint64_t timestamp;
        uint64_t primary_key() const { return key; }
        uint64_t by_Id() const { return Id; }

    };

    typedef multi_index<"entry"_n, entry, indexed_by<"Id"_n, const_mem_fun<entry, uint64_t, &entry::by_Id>>> ledger_table;

    using set_action = action_wrapper<"rcrdtfr"_n, &Ledger::rcrdtfr>;

    ledger_table ledger;
};

EOSIO_DISPATCH(Ledger,(rcrdtfr))