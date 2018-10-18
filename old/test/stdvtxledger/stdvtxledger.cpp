#include <eosiolib/eosio.hpp>
#include <eosiolib/print.hpp>
using namespace eosio;

class Ledger : public contract {
  public:
      using contract::contract; 	  
      /// @abi action
      void init()
      {
          print("Reinitialize contract");
      }
};

EOSIO_ABI( Ledger, (init))


