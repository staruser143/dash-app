# Step 1: Pull the PostgreSQL image
docker pull postgres

# Step 2: Run the container
docker run --name my_postgres_container -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -v my_local_data_directory:/var/lib/postgresql/data -d postgres

docker exec -it my_postgres_container bash

psql -U postgres

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
CREATE DATABASE database_name;
\l
\c database_name
\dt 
\dt *.* 

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL
);
INSERT INTO employees (name, department)
VALUES ('John Doe', 'Engineering');

docker pull dpage/pgadmin4

docker run -p 80:80 \
    -e 'PGADMIN_DEFAULT_EMAIL=sridharb.in@gmail.com' \
    -e 'PGADMIN_DEFAULT_PASSWORD=Carter143$' \
    -e 'PGADMIN_DEFAULT_PASSWORD=Carter143$' \
    -e 'PGADMIN_LISTEN_PORT=8080' \
    -e 'PGADMIN_CONFIG_PROXY_X_HOST_COUNT=1' \
    -e 'PGADMIN_CONFIG_PROXY_X_PREFIX_COUNT=1' \
    -d dpage/pgadmin4

