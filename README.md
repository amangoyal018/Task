# Task
API Autocomplete System - Technical Assignment


# Approach
Tested different endpoints (/v1, /v2, /v3) to understand responses and constraints.
Used a prefix-based approach to systematically extract names.
Implemented delays to avoid hitting request limits.
Collected all results and counted the number of words and requests for each endpoint.
If "s" returns 15 names, we explore "s ", "s+", "s-", "s0", "s1", ..., "sz", etc. (in v3)

# Findings

There were 3 different endpoints v1 v2 v3
v1 - alphabets
v2 - alphanumeric
v3 - alphanumeric and symbols like(+-.)

There was different threshold limit for each endpoint.
If for some prefix there are many words, v1 shows 10 , v2 - 12 and v3 - 15 words which inturn more recursive call to find exact words.

For each query it return a json which contains version count and results(all words).

When querying an invalid prefix, sometimes the API returns
{"detail": "Not Found"}


# Challenges & Solutions

Initially there were error (429) due to too many request that was 100 words per minute.
{"detail":"100 per 1 minute"}
Introduced a 0.6-second delay (time.sleep(0.6)) between requests.

The API was handling "a" , "a+" , "a " as same as it trims the white space so encoded the prefix properly so that + be treated as %2B not %20


# Results
For v1:
Request Made:
Words found:

For v2:
Request Made:
Words found:

For v3:
Request Made:
Words found: