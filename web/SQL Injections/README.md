# SQL Injection #
## what is SQL? ##
sql is a quary language for database management,  
what does it mean?  
if the user have a table of users (the server saves the username and passwords of each user)

| username | password |
| -------- | -------- |
| bob      | bob\_p   |
| alice    | alice\_p |

we can add user with the command  
```SQL
INSERT INTO users ('username', 'password') valuse ('eve', 'eve_p')
```
Most important for our specific case we need to know the quary to find a user (for example, if a user enter thier username and password, we need to check if there are a user with the givin username and password).  

```SQL
SELECT * FROM users WHERE username='eve' AND password='eve_p'
```

one more thing we need to know is that a comment is possible in SQL with `--` for examle, here the same quary as before
```SQL
SELECT * FROM users WHERE username='eve' AND password='eve_p' -- this it a comment
```

## SQL Injection ##
As a pyton developer, I build the quary from the user input. for example if I have a variables `username` and `password` and I want to know if the user exists in the database, I'll do something like this:

```python
c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
```

what is the problem then?  
the problem is that with the right input the user can manipulate the quary.  
for example, I can Login to bob's account just by knowing his username. By entering `bob'--` in the username and `not relevant` as password the quary will look like this:

```SQL
SELECT * FROM users WHERE username='bob'--' AND password='not relevant'
```

another way can be to enter `bob` as username and `'or'1'='1` as password, then we can get the next quary:

```SQL
SELECT * FROM users WHERE username='bob' AND password='' OR '1'='1'
```

this quary will fatch all the users (not just bob) because OR come after AND in SQL

