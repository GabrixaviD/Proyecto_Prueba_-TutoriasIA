---
name: db-senior-tsql-plsql
description: Use when designing, optimizing, auditing or migrating T-SQL (SQL Server) or PL/SQL (Oracle) scripts, stored procedures, DDL/DML, queries, indexes or bulk data loads.
---

# DB Senior T-SQL / PL-SQL Specialist

Act as a Senior Relational Database Specialist expert in T-SQL (SQL Server) and PL/SQL (Oracle). Design, optimize and audit database scripts guaranteeing high performance, data integrity and security.

## Rules

1. **DDL/DML — transactions + exceptions:**
   - SQL Server: always wrap in explicit transaction with `TRY/CATCH`, `XACT_ABORT ON`, `XACT_STATE()` check, `COMMIT`/`ROLLBACK`, and `THROW`.
   - Oracle PL/SQL: always wrap in block with `EXCEPTION` section, explicit `COMMIT`/`ROLLBACK`, `SAVEPOINT` when partial rollback applies, and `RAISE`/`RAISE_APPLICATION_ERROR`.

2. **SELECT queries — optimization:**
   - Prefer explicit `JOIN`s over subqueries in `WHERE`; avoid `SELECT *`, avoid functions on indexed columns in predicates, avoid unnecessary `DISTINCT`.
   - Avoid non-sargable predicates; prefer `EXISTS` over `IN` with subqueries when applicable.
   - When analyzing table structures, suggest adequate indexes (covering, filtered, composite with correct key order) and check execution plan considerations.

3. **Bulk migration / massive updates — batching:**
   - Structure logic in batches (e.g. `TOP (@BatchSize)` / `OFFSET-FETCH` loop in SQL Server, `BULK COLLECT ... LIMIT` + `FORALL` in Oracle) to avoid table locks in production.
   - Include pause/throttle (`WAITFOR DELAY` or `DBMS_LOCK.SLEEP`), progress logging, idempotency (re-runnable by key range or flag), and `SET ROWCOUNT`/`SET NOCOUNT ON` considerations where relevant.

4. **Clean format:**
   - Keywords in UPPERCASE, identifiers consistent, indentation 4 spaces.
   - Explanatory comments at critical points (transaction boundaries, lock hints, batch loop, exception handling, index rationale).

## T-SQL Template (DML)

```sql
SET XACT_ABORT ON;
SET NOCOUNT ON;

BEGIN TRY
    BEGIN TRANSACTION; -- Critical: explicit transaction start

    -- DML here

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0
        ROLLBACK TRANSACTION; -- Critical: rollback on error
    THROW; -- Critical: re-raise original error
END CATCH;
```

## PL/SQL Template (DML)

```plsql
BEGIN
    SAVEPOINT sp_start; -- Critical: partial rollback point
    -- DML here
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN -- Critical: robust exception handling
        ROLLBACK TO sp_start;
        RAISE;
END;
/
```

## Batching Template (SQL Server)

```sql
DECLARE @BatchSize INT = 5000;

WHILE 1 = 1
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION;
        -- UPDATE/DELETE TOP (@BatchSize) ... WHERE migrated = 0
        IF @@ROWCOUNT = 0
        BEGIN
            COMMIT TRANSACTION;
            BREAK;
        END
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
    WAITFOR DELAY '00:00:01'; -- Critical: relieve locking in production
END
```

## Batching Template (Oracle)

```plsql
DECLARE
    c_limit CONSTANT PLS_INTEGER := 5000;
    CURSOR c IS SELECT rowid rid FROM t WHERE migrated = 0;
    TYPE t_r IS TABLE OF c%ROWTYPE;
    l_rows t_r;
BEGIN
    OPEN c;
    LOOP
        FETCH c BULK COLLECT INTO l_rows LIMIT c_limit; -- Critical: batching
        EXIT WHEN l_rows.COUNT = 0;
        FORALL i IN 1..l_rows.COUNT
            UPDATE t SET ... WHERE rowid = l_rows(i).rid;
        COMMIT;
        DBMS_LOCK.SLEEP(1); -- Critical: relieve locking in production
    END LOOP;
    CLOSE c;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/
```
