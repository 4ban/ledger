Eos = require('eosjs')
let Ledger = require('./vltxldgr');


config = Ledger.config('cf057bbfb72640471fd910bcb67639c22df9f92470936cddc1ade0e2f2e7dc4f', '5KfpCFGR8SBZ3At7oGTDcHgzXgCZRGV6hCT7DTfReYQ63gi3gQz', 'http://127.0.0.1:8888', 60, true, true, true );

ledger = Eos(config)

Ledger.rcrdtrf(ledger, "test", "Distribution", "Trust", 1234, 1234, 1234);