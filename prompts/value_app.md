1. create a sqllite local database in the value/data directory, called value.

Create the table stock:

- symbol (pk)
- name (str)

Create the table keyvalue:

- symbol (fk)
- key (str)
- value (str)

2. use search to fill the table 'stock' with stocks from the US, Europe and Asia that are part of one of the large cap indices.
- In the US, use Nasdaq 100, SP 500 and dow jones
- In Europe and Asia, use the leading market-cap ranked indices for the 5 largest economies
In the keyvalue table, fill in the values
- market_cap in USD
- current share price in USD