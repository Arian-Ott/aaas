# Generating Keys

Run the following commands to generate ECC Keys
```bash
openssl ecparam -name secp521r1 -genkey -noout -out ec-private.pem

openssl ec -in ec-private.pem -pubout -out ec-public.pem
```

>[!caution] Attention
>Never share the `ec-private.pem` with anyone
