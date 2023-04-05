# calculator
direct contact me if you have any question
## structre
```
+---------------+
|               |
|               |
|    <ROOT>     |
|               |
|               |
+--------+------+
         |
         |
         |
         |
         |                                    +--------------------------------+
         |                                    |                                |
         +------------------------------------+                                |
         |                                    |      backend                   |
         |                                    |                                |
         |                                    |                                |
         |                                    |                                |
         |                                    +--------------------------------+
         |
         |
         |
         |
         |
         |
         |
         |
         |
         |
         |
         |
         |
         |                                    +----------------------------------+
         |                                    |                                  |
         |                                    |                                  |
         +------------------------------------+                                  |
                                              |        frontend                  |
                                              |                                  |
                                              |                                  |
                                              +----------------------------------+
```

### backend
---
backend is a fastAPI project.
once it run, you can find endpoint doc in /docs
build is passed and verifyied in windows x64 and ARMv7

how to run:
- cd into the project dir which is ./backend
- make sure postgresDB is up and running
  - if need one. samply install docker and run `docker run  --env=POSTGRES_USER=dba --env=POSTGRES_PASSWORD=qwerasdf --env=POSTGRES_DB=loanpro   --volume=postgres_data:/var/lib/postgresql/data --volume=/var/lib/postgresql/data -p 5432:5432 -d postgres:15.1`
 - make sure dependcy list below are all installed
 - depends on you OS run start command
  - windows: `python.exe -m uvicorn main:app --reload `
  - mac/linux: likely `python3 -m uvicorn main:app`
---

--- 
requirments and assumptions
---
- use python3
- use venv or other envirment management
- run `pip install -r requirements.txt` to download lib
- needs a postgresDB instance defined in main.py
- needs uvicorn
- recommend IDE: PyCharm

---
faq and misc
---
- got connection timeout when start the application
  - check DB config
- got dependecy failure
  - run `pip install -r requirements.txt` in the correct envirments
- got access denied while work with frontend
  - check CROS setting in main.py
  
### frontend
---
frontend is Vue2 project

how to run:
- make sure you meet the requirments list below
- cd into the project dir `./frontend/calculator/`
- run `npm serve`
- access the url showed

---

---
requirments and assumptions
---
- need nodejs and npm
- need modern browser like chrome or firefox
- need `npm install` to gei dependecy
- need correct .env setting

---
faq and misc

TBD
---

