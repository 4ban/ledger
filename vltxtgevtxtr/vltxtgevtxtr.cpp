#include <eosiolib/eosio.hpp>
#include <eosiolib/multi_index.hpp>
#include <eosiolib/types.hpp>
#include <string>
#include <eosiolib/transaction.hpp>
#include<eosiolib/time.hpp>

using namespace eosio;

class Ledger: public contract {
	public:
		Ledger(account_name s) :
				contract(s), ledger(s, s){

		}
		using contract::contract;
		[[eosio::action]]
		void rcrdtfr(account_name s, std::string fromaccount,
				std::string toaccount, float amount, std::string fromkey,
				std::string tokey, std::string comment, std::string nonce) {
			uint64_t iVal = amount;
			float tempfVal = amount - iVal;
			uint64_t fVal = tempfVal * 100000000;
			int64_t negAmount = -1 * amount;
			int64_t posAmount = amount;

			int64_t negiVal = -1 * amount;
			int64_t posiVal = amount;

			int64_t negfVal = -1 * fVal;
			int64_t posfVal = fVal;

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
				p.fromKey = "";
				p.amount = negAmount;
				p.iVal = negiVal;
				p.fVal = negfVal;
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
				p.fromKey = "";
				p.amount = posAmount;
				p.iVal = posiVal;
				p.fVal = posfVal;
				p.comment = comment;
				p.nonce = nonce;
				p.tbn = tbn;
				p.tbp = tbp;
				p.timestamp = timestamp;
			});

		}

	private:

		struct [[eosio::table]] entry {
				account_name s;
				uint64_t key = 0;
				uint64_t Id = 0;
				std::string sToKey;
				std::string fromAccount;
				std::string toAccount;
				std::string fromKey;
				int64_t amount;
				int64_t iVal;
				foat fVal;
				std::string comment;
				std::string nonce;
				int64_t tbn;
				int64_t tbp;
				uint64_t timestamp;
				uint64_t primary_key() const {
					return key;
				}
				uint64_t by_Id() const {
					return Id;
				}

		};
		typedef eosio::multi_index<N(entry), entry,
				indexed_by<N(Id), const_mem_fun<entry, uint64_t, &entry::by_Id>>> ledgertable;
		ledgertable ledger;


};

EOSIO_ABI( Ledger,(rcrdtfr))
