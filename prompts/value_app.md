goal: make an application called Value that identifies value stocks by using agentic ai.

0. write all steps in a plan execution.md before you start to generate code. during the writing of execution.md I expect you to ask me questions and not blindly start to fill in the gaps.

1. data structure
   make a new supabase database
   tables: stock, insider, advise, user, system

- stock has the fields symbol, name and type. type is an enumeration of "value|insider|candidate"
- insider is an inside trader such as eric trump jr. or nancy pelosi
- advise can store buy advises, based on the following criteria:

1. an inside trader bought the stock
2. the stock identifies as a value stock and is underpriced
3. the stock can be a candidate to be added to an index soon, such as the sp 500 or the nasdaq 100
   advise has a datetime field and a general comments textfield

- user is a user that can login to the Value app. User is identified by a gmail account.
  make the tables directly in supabase, apply indices where required.
- system is a property bag, similar to system in the autobalance app. copy the values for the servers we currently use in autobalance, including the friendly server names

2. App

- build in flutter, hosted in firebase. Backend is supabase.
- make a program directory 'firebase' in the value directory
- make a deploy script in the root of the value directory. use the same functionality as the autobalance app: automatic git sync. only build for web and mobile web. Deploy both flutter and the agentic daemon (see below)
- homescreen: chronologic list of last advices
- menu: make a menu option for each table to perform CRUD operations with a pager.

3. Agentic daemon
   the agentic part is a batch job that runs a python process on one of the ubuntu servers. It connects to deepseek v4 flash and asks it to perform various tasks. it runs in a terminal on ubuntu 1 so we can see what it is doing.

3A. value stock list
at initialisation, and thereafter once a week, it creates the list of value stocks: the 100 stocks globally with the largest market cap in either the us, europe or asia

3B. inside trader list
at initialisation, and thereafter once a week, it creates a list of all the insiders in the US congress, senate, relatives of us congress or senate members, or the extend trump cabinet and trump family that execute insider trades. the script identifies the natural persons and any company/trust/other entity that executes these trades.

3C. index candidates list
at initialisation, and thereafter once a week, it looks for all the stocks that may be included in an index in the next period.

4. Agentic daemon advise
   4A. Value stock advise
   run once a day during trading sessions.
   in a single prompt, for all the value stocks, identify those stocks that have decreased in value by more than 10% in the last 5 trading days. for each stock, make an advise record. For stocks that have been identified previously in the last 5 days, do not repeat the advise.

4B. insider advise
run once a day during trading sessions.
Find all the stocks that have been traded by the insiders.
for each insider, for each stock, create an advise line. For stocks that have been identified as insider trades, do not repeat the advise

4C. index candidates
run once a week during trading sessions.
in a single prompt, for all the value stocks, identify those stocks that are potentially candidates to be included in an index in the USA, Canada, Europe or Asia. Make an advise record.

5. Other
   use the pushover/ntfy functionality from autobalance to notify the users of any advises.
