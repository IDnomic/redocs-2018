# redocs-2018
Towards a decentralized identity management solution based on Blockchain

# Blockchain initialization
To create a new blockchain using multichain:

`$ ./multichain-util create chain1`
`$ ./multichaind chain1`

From a new node, to join the same blockchain:

`$ ./multichaind chain1@ip-first-node:port`

To display public keys from a node:

`$ ./multichain-cli chain1 getaddresses`

To grant mining access to public key:

`$ ./multichain-cli chain1 grant mine`

To create stream1 with closed access (only this miner can write to it):

`$ ./multichain-cli chain1 create stream stream1 false`

To subscribe to a stream (allows to write to it):

`$ ./multichain-cli chain1 subscribe stream1`



## Scripts part
Write into `~/.multichain/chain1/multichain.conf` (for easier scripting):

```
rpchost=localhost
rpcport=port --> port returned when launching ./multichaind
```

To insert a certificate in the blockchain:

`$ python3 mclib/insert.py "certificate" path_to_certificate.crt`

To start webserver listening for webextension queries:

`$ python3 mclib/chainserver.py`

Server will listen on 0.0.0.0:8080

## Webextension

Launch firefox, open about:debugging. THen click "load temporary extension" and select "manifest.json". Extension button will appear next to the url bar. By visiting an HTTPS website, the extension will retrieve the certificates, get their sha256 fingerprint and ask for the webserver if they are in the blockchain. Then, depending on the answer, a check mark or red cross will appear as the button badge. By clicking the button, you can check which certificate has been validated or not.