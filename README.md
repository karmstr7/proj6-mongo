# README

## Proj6-Mongo
## Authors:
#### Michal Young
#### Revised by: Keir Armstrong

#### About:
- Use MongoDB as exercise for permanent data storage.
- A web app which lets the user make memos.
- Memos are arranged from oldest to furthest in the future.

#### Activation:
- In /memos create a credentials.ini file, and fill in the following variables:
    1. SECRET_KEY
    2. PORT
    3. DB_USER
    4. DB_USER_PW
    5. DB_HOST
    6. DB_PORT
    7. DB
- After credentials.ini has been created,
enter 'make install' under the main directory to install virtual environment.
- Enter 'make start' to start the server.
- Enter 'make stop' to stop the server from running.
- Enter 'make test' to run test cases.