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

		Ledger(name self, name code, datastream<const char*> ds):contract(self, code, ds) {}
		// The constructor below throw an error
		// Ledger(name s, name code,  datastream<const char*> ds): contract(s, code, ds), ledger(s, s.value) {}


		ACTION rcrdtfr(const name self,
									string fromaccount,
									string toaccount,
									double amount,
									string tokey,
									string comment,
									string nonce) {

			double negAmount = -1 * amount;
			double posAmount = amount;

			uint64_t tbn = tapos_block_num();
			uint64_t tbp = tapos_block_prefix();
			uint64_t timestamp = current_time();

			ledgertable ledger(_self, _self);

			ledger.emplace(get_self(), [&](auto& p)
			{
				p.key = ledger.available_primary_key() + 1;
				p.Id = ledger.available_primary_key() + 1;
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
				p.key = ledger.available_primary_key() + 1;
				p.Id = ledger.available_primary_key() + 1;
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
				name self;
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

				// EOSLIB_SERIALIZE( rcrdtfr, (s)(key)(Id)(sToKey)(fromAccount)(toAccount)(amount)(comment)(nonce) )
		};

		typedef multi_index<"entry"_n, entry, indexed_by<"Id"_n, const_mem_fun<entry, uint64_t, &entry::by_Id>>> ledgertable;

		using set_action = action_wrapper<"rcrdtfr"_n, &Ledger::rcrdtfr>;

		ledgertable ledger;

};

EOSIO_DISPATCH( Ledger,(rcrdtfr))
