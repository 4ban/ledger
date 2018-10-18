Eos = require('eosjs')
config = {
  chainId: 'cf057bbfb72640471fd910bcb67639c22df9f92470936cddc1ade0e2f2e7dc4f', 
  keyProvider: '5KfpCFGR8SBZ3At7oGTDcHgzXgCZRGV6hCT7DTfReYQ63gi3gQz', 
  httpEndpoint: 'http://ec2-35-183-119-153.ca-central-1.compute.amazonaws.com:8888',
    debug: false,
    expireInSeconds: 60,
  logger: {
    log: null,
    error: null
  },
}
eos = Eos(config)
eos.contract('vtxledger').then(vtxledger =>{vtxledger.getblnc(
        {
          "account":"vtxtrust",
          "tokey":"EOS62L2r4FqnCbHAspPS3KBByGa728G3UDYxGkTY15mad97M4JhzN",
        },
        {
             'authorization':['vtxledger@active']
        }).then(result =>{console.log(JSON.stringify(result, null, 4))})
      }
)


