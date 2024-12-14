# Commands useful for PostgreSQL DB Operations

### Connect to a database:

    ```sql
    psql -h hostname -d databasename -U username -W
    psql -U postgres -d kahani_db
    ```

    -h: hostname of the machine where the database is running
    -d: name of the database to connect to
    -U: username to connect as
    -W: force psql to prompt for a password
    ```

### List all databases:

    ```sql
    \l
    ```

### Exit psql:

    ```sql
    \q
    ```

### Reading a DB

    ```sql
    \l
    ```

### Check which DB is it

    ```sql
    \c
    ```

### Switcing to another DB

    ```sql
    \c <db_name>
    ```

## List all tables in the current database:

    ```sql
    \dt
    ```

### Looking inside a table

    ```sql
    \dt <table_name>
    ```

### Updating a Table

    ```sql
    UPDATE <table_name> SET <column_name> = <value> WHERE <condition>
    ```

### fetching table data

    ```sql
    SELECT column1, column2 FROM tablename;
    ```

### with where clause

    ```sql
    SELECT column1, column2 FROM tablename; WHERE <condition>
    ````

### Insert data into a table

    ```sql
    INSERT INTO table_name (column1, column2, column3, ...)
    VALUES (value1, value2, value3, ...);
    ```

### Delete data from a table:

    ```sql
    DELETE FROM table_name WHERE condition;
    ```

### Create a new table:

    ```sql
    CREATE TABLE table_name (
        column1 datatype,
        column2 datatype,
        column3 datatype,
        ....
    );
    ```

### Drop a table:

    ```sql
    DROP TABLE table_name;
    ```

### Add a new column to a table:

    ```sql
    ALTER TABLE table_name
    ADD column_name datatype;
    ```

### Delete a column from a table:

    ```sql
    ALTER TABLE table_name
    DROP COLUMN column_name;
    ```

### Rename a table:

    ```sql
    ALTER TABLE table_name
    RENAME TO new_table_name;
    ```

### Rename a column:

    ```sql
    ALTER TABLE table_name
    RENAME COLUMN column_name TO new_column_name;
    ```

### Count the number of rows in a table:

    ```sql

    SELECT COUNT(*) FROM table_name;
    ```

### Get the maximum value from a column:

    ```sql
    SELECT MAX(column_name) FROM table_name;
    ```

### Get the minimum value from a column:

    ```sql

    SELECT MIN(column_name) FROM table_name;
    ```

### Create an index on a table:

        ```sql
        CREATE INDEX index_name
        ON table_name (column_name);
        ```

### Remove an index:

    ```sql
    DROP INDEX index_name;
    ```

### List all indexes on a table:

    ```sql
    \di table_name;
    ```
