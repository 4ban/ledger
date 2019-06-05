
#include "crowdfledger.hpp"

void crowdfledger::rcrdtfr(name from, name to, asset quantity, string tokey, string comment, string nonce) {
    // Parameters validation
    check(quantity.is_valid(), "Invalid quantity");
    check(quantity.amount > 0, "Must transfer positive amount");
    check(from == to, "From and To fields should be different.");

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

void crowdfledger::updatetfr(uint64_t id, name from, name to, asset quantity, string tokey, string comment, string nonce) {
    check(id > 0, "ID should be positive");
    check(quantity.is_valid(), "Invalid quantity");
    check(quantity.amount > 0, "Must transfer positive amount");
    check(from == to, "From and To fields should be different.");

    transactions_index transactions(_self, _self.value);
    uint64_t timestamp = current_time();
    auto toupdate = transactions.find(id);

    transactions.modify(toupdate, _self, [&](auto &row) {
        row.from = from;
        row.to = to;
        row.quantity = quantity;
        row.tokey = tokey;
        row.comment = comment;
        row.nonce = nonce;
        row.timestamp = timestamp;
    });
}

void crowdfledger::deletetfr(uint64_t id) {
    check(id > 0, "ID should be positive");
    transactions_index transactions(_self, _self.value);
    auto todelete = transactions.find(id);
    check(todelete != transactions.end(), "ID does not exist");
    transactions.erase(todelete);
}

EOSIO_DISPATCH(crowdfledger, (rcrdtfr)(updatetfr)(deletetfr))