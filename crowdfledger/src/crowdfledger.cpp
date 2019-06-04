
#include "crowdfledger.hpp"

void crowdfledger::rcrdtfr(name from,
                            name to,
                            asset quantity,
                            string tokey,
                            string comment,
                            string nonce) {

    transactions_index transactions(_self, _self.value);
    uint64_t timestamp = current_time();
    transactions.emplace(_self, [&](auto &row) {
        row.id = transactions.available_primary_key();
        row.from = from;
        row.to = to;
        row.quantity = quantity;
        row.tokey = tokey;
        row.comment = comment;
        row.nonce = nonce;
        row.timestamp = timestamp;
    });
}

EOSIO_DISPATCH(crowdfledger, (rcrdtfr))