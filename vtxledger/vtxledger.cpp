﻿#include <eosiolib/eosio.hpp>
#include <eosiolib/multi_index.hpp>
#include <eosiolib/types.hpp>
#include <string>
#include <sstream>
#include <iostream>

using namespace eosio;

class Ledger: public contract {
	public:
		Ledger(account_name s) :
				contract(s), ledger(s, s) {

		}

		/// @abi action
		void getentries() {
			int64_t amount = 0;
			for (auto& item : ledger) {
				std::string s;
				s.append("{");
				s.append("'fromaccount'");
				s.append(":");
				s.append(item.fromAccount);
				s.append(", ");
				s.append("'toaccount'");
				s.append(":");
				s.append(item.toAccount);
				s.append(", ");
				s.append("'fromkey'");
				s.append(":");
				s.append(item.fromKey);
				s.append(", ");
				s.append("'tokey'");
				s.append(":");
				s.append(item.sToKey);
				s.append(", ");
				s.append("'amount'");
				s.append(":");
				s.append(std::to_string(item.amount));
				s.append("}");
				print(s.c_str());

			}
		}
		/// @abi action
		void getblnc(std::string account, std::string tokey) {
			int64_t amount = 0;
			//always account name
			if (tokey.compare("") == 0) {
				for (auto& item : ledger) {
					if (item.fromAccount.compare(account) == 0
							|| item.toAccount.compare(account) == 0) {
						amount += item.amount;
					}
				}
			} else {
				for (auto& item : ledger) {
					if ((item.fromAccount.compare(account) == 0
							|| item.fromKey.compare(tokey) == 0))
						amount += item.amount;
				}
				for (auto& item : ledger) {
					if (item.sToKey.compare(tokey) == 0
							|| item.toAccount.compare(account) == 0)
						amount += item.amount;
				}
			}

			int build = 0;
			std::string s;
			s.append("{");
			s.append("'amount'");
			s.append(":");
			s.append(std::to_string(abs(amount)));
			s.append(", ");
			s.append("'currency'");
			s.append(":");
			s.append("'VTX'");
			s.append("}");
			print(s.c_str());
		}

		/// @abi action
		void retrvtxns(std::string account, std::string tokey, uint64_t limit) {

			int i = 0;
			uint64_t count = 1;
			std::string str;

			for (auto& item : ledger) {

				str.append("{");
				str.append("\"""fromaccount""\"");
				str.append(":");
				str.append("\"" + item.fromAccount + "\"");
				str.append(",");
				str.append("\"""toaccount""\"");
				str.append(":");
				str.append("\"" + item.toAccount + "\"");
				str.append(",");
				str.append("\"""fromkey""\"");
				str.append(":");
				str.append("\"" + item.fromKey + "\"");
				str.append(",");
				str.append("\"""tokey""\"");
				str.append(":");
				str.append("\"" + item.sToKey + "\"");
				str.append(",");
				str.append("\"""amount""\"");
				str.append(":");
				str.append("\"" + std::to_string(item.amount) + "\"");
				str.append("}");
				if (count >= limit)
					break;
				++count;
				str.append(",");
			}
			std::string finalstring;
			finalstring.append("[");
			finalstring.append(str);
			finalstring.append("]");
			print(finalstring);

		}

		/// @abi action
		void rcrdtfr(account_name s, std::string fromaccount,
				std::string toaccount, uint64_t amount, std::string fromkey,
				std::string tokey) {

//require_auth(s);
			uint64_t lKey = string_to_name(tokey.c_str());
			uint64_t lSecKey = string_to_name(toaccount.c_str());
//eosio_assert(amount != 0, "amount needs to be greater than 0");

			bool condition1 = false;
			bool condition2 = false;
			bool condition3 = false;
			bool condition4 = false;
			bool condition5 = false;
			bool condition6 = false;

//All fields missing - No transaction
			condition1 = !fromaccount.empty() && !toaccount.empty()
					&& !fromkey.empty() && !tokey.empty();

//eosio_assert(condition1, "all fields missing");
//2 first fields missing - No transaction
			condition2 = fromaccount.empty() || toaccount.empty();
//eosio_assert(condition2, "missing toaccount or fromaccount or both");

//All fields full - Wallet to Wallet
			condition3 = !fromkey.empty() && !tokey.empty();

//fromkey field missing - Account to Wallet
			condition4 = fromkey.empty() && !tokey.empty();

//tokey field missing - Wallet to Account
			condition5 = !fromkey.empty() && tokey.empty();

//tokey fields missing - Account to Account
			condition6 = fromkey.empty() && tokey.empty();

			int64_t negAmount = -1 * amount;
			int64_t posAmount = amount;
//Wallet to Wallet
			if (condition3) {
				//decrease with fromkey
				print("Wallet to Wallet");
				//check for funds
				//eosio_assert(getbalance(fromaccount,fromkey) <= amount, "Not enough funds in account");
				ledger.emplace(get_self(), [&](auto& p)
				{
					p.key = ledger.available_primary_key();
					p.Id = ledger.available_primary_key();
					p.fromAccount = fromaccount;
					p.toAccount = "";
					p.toKey = lKey;
					p.sToKey = "";
					p.fromKey = fromkey;
					p.amount = negAmount;

				});
				//increase with toKey
				ledger.emplace(get_self(), [&](auto& p)
				{
					p.key = ledger.available_primary_key();
					p.Id = ledger.available_primary_key();
					p.fromAccount = "";
					p.toAccount = toaccount;
					p.toKey = lKey;
					p.sToKey = tokey;
					p.fromKey = "";
					p.amount = posAmount;
				});
			}
			//Account to Wallet
			else if (condition4) {
				print("Account to Wallet");

				//check for funds
				eosio_assert(getbalance(fromaccount, "") >= amount,
						"insufficient_funds");
				//decrease with fromaccount
				ledger.emplace(get_self(), [&](auto& p)
				{
					p.key = ledger.available_primary_key();
					p.Id = ledger.available_primary_key();
					p.fromAccount = fromaccount;
					p.toAccount = "";
					p.toKey = lKey;
					p.sToKey = "";
					p.fromKey = "";
					p.amount = negAmount;

				});
				//increase with tokey
				ledger.emplace(get_self(), [&](auto& p)
				{
					p.key = ledger.available_primary_key();
					p.Id = ledger.available_primary_key();
					p.fromAccount = "";
					p.toAccount = toaccount;
					p.toKey = lKey;
					p.sToKey = tokey;
					p.fromKey = "";
					p.amount = posAmount;

				});
			}
			//Wallet to account
			else if (condition5) {
				print("Wallet to account");
				//decrease with fromaccount
				//check for funds
//				if (getbalance(fromaccount,"") >= 0){
//					print("Insufficient funds");
//					return;
//				}

				////eosio_assert(getbalance(fromaccount,"") <= 0, "Not enough funds in account"));
				eosio_assert(getbalance(fromaccount, fromkey) >= amount,
						"insufficient_funds");

				//decrease with fromaccount
				ledger.emplace(get_self(), [&](auto& p)
				{
					p.key = ledger.available_primary_key();
					p.Id = ledger.available_primary_key();
					p.fromAccount = fromaccount;
					p.toAccount = "";
					p.toKey = lKey;
					p.sToKey = "";
					p.fromKey = fromkey;
					p.amount = negAmount;

				});
				//increase with to account
				ledger.emplace(get_self(), [&](auto& p)
				{
					p.key = ledger.available_primary_key();
					p.Id = ledger.available_primary_key();
					p.fromAccount = "";
					p.toAccount = toaccount;
					p.toKey = lKey;
					p.sToKey = "";
					p.fromKey = "";
					p.amount = posAmount;

				});
			}
			//Account to Account
			else if (condition6) {
				print("Account to Account");

				//check for funds
				//eosio_assert(getbalance(fromaccount,"") >= amount, "Not enough funds in account");
				//decrease from account
				ledger.emplace(get_self(), [&](auto& p)
				{
					p.key = ledger.available_primary_key();
					p.Id = ledger.available_primary_key();
					p.fromAccount = fromaccount;
					p.toAccount = "";
					p.toKey = lKey;
					p.sToKey = "";
					p.fromKey = "";
					p.amount = amount;
				});
				//augment toaccount
				ledger.emplace(get_self(), [&](auto& p)
				{
					p.key = ledger.available_primary_key();
					p.Id = ledger.available_primary_key();
					p.fromAccount = "";
					p.toAccount = toaccount;
					p.toKey = lKey;
					p.sToKey = "";
					p.fromKey = "";
					p.amount = posAmount;
				});

			}
			//Init Account TODO: assign initially
			else if (false) {
				print("INIT");
				//increase fromaccount
				ledger.emplace(get_self(), [&](auto& p)
				{
					p.key = ledger.available_primary_key();
					p.Id = ledger.available_primary_key();
					p.fromAccount = fromaccount;
					p.toAccount = "";
					p.toKey = lKey;
					p.sToKey = "";
					p.fromKey = "";
					p.amount = 364000000000;
				});
			}

		}

		int getbalance(std::string account, std::string tokey) {
			int64_t amount = 0;
			//always account name
			if (tokey.compare("") == 0) {
				for (auto& item : ledger) {
					if (item.fromAccount.compare(account) == 0
							|| item.toAccount.compare(account) == 0) {
						amount += item.amount;
					}
				}
			} else {
				for (auto& item : ledger) {
					if ((item.fromAccount.compare(account) == 0
							|| item.fromKey.compare(tokey) == 0))
						amount += item.amount;
				}
				for (auto& item : ledger) {
					if (item.sToKey.compare(tokey) == 0
							|| item.toAccount.compare(account) == 0)
						amount += item.amount;
				}
			}

			return amount;
		}

	private:

		/// @abi table
		struct entry {
				account_name s;
				uint64_t key;
				uint64_t Id;
				std::string sToKey;
				std::string fromAccount;
				std::string toAccount;
				uint64_t toKey;
				std::string fromKey;
				int64_t amount;

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

EOSIO_ABI( Ledger,(getblnc)(rcrdtfr)(retrvtxns)(getentries))
