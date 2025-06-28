TABLES_VIEWS = [

    """DROP TABLE IF EXISTS dept_emp""",

    """DROP TABLE IF EXISTS dept_manager""",

    """DROP TABLE IF EXISTS titles""",

    """DROP TABLE IF EXISTS salaries""",

    """DROP TABLE IF EXISTS employees""",

    """DROP TABLE IF EXISTS departments""",

    """CREATE TABLE employees (
        emp_no      INTEGER  NOT NULL PRIMARY KEY,
        birth_date  TEXT     NOT NULL,
        first_name  TEXT     NOT NULL,
        last_name   TEXT     NOT NULL,
        gender      TEXT     NOT NULL CHECK(gender IN ('M', 'F')),   
        hire_date   TEXT     NOT NULL
        
    );""",

    """CREATE TABLE IF NOT EXISTS departments (
        dept_no     TEXT        NOT NULL PRIMARY KEY,
        dept_name   TEXT        NOT NULL UNIQUE
    );""",

    """CREATE TABLE IF NOT EXISTS dept_manager (
        emp_no       INTEGER     NOT NULL,
        dept_no      TEXT        NOT NULL,
        from_date    TEXT        NOT NULL,
        to_date      TEXT        NOT NULL,
        FOREIGN KEY (emp_no) REFERENCES employees (emp_no) ON DELETE CASCADE,
        FOREIGN KEY (dept_no) REFERENCES departments (dept_no) ON DELETE CASCADE,
        PRIMARY KEY (emp_no, dept_no)
    );""",

    """CREATE TABLE IF NOT EXISTS dept_emp (
        emp_no      INTEGER     NOT NULL,
        dept_no     TEXT        NOT NULL,
        from_date   TEXT        NOT NULL,
        to_date     TEXT        NOT NULL,
        FOREIGN KEY (emp_no) REFERENCES employees (emp_no) ON DELETE CASCADE,
        FOREIGN KEY (dept_no) REFERENCES departments (dept_no) ON DELETE CASCADE,
        PRIMARY KEY (emp_no, dept_no)
    );""",

    """CREATE TABLE IF NOT EXISTS titles (
        emp_no      INTEGER     NOT NULL,
        title       TEXT        NOT NULL,
        from_date   TEXT        NOT NULL,
        to_date     TEXT,
        FOREIGN KEY (emp_no) REFERENCES employees (emp_no) ON DELETE CASCADE,
        PRIMARY KEY (emp_no, title, from_date)
    );""",

    """CREATE TABLE IF NOT EXISTS salaries (
        emp_no      INTEGER     NOT NULL,
        salary      INTEGER     NOT NULL,
        from_date   TEXT        NOT NULL,
        to_date     TEXT        NOT NULL,
        FOREIGN KEY (emp_no) REFERENCES employees (emp_no) ON DELETE CASCADE,
        PRIMARY KEY (emp_no, from_date)
    );""",

    # Drop existing views before recreating (since SQLite doesn't support CREATE OR REPLACE VIEW)
    """DROP VIEW IF EXISTS dept_emp_latest_date;""",
    
    """CREATE VIEW dept_emp_latest_date AS
        SELECT emp_no, MAX(from_date) AS from_date, MAX(to_date) AS to_date
        FROM dept_emp
        GROUP BY emp_no;""",
    
    """DROP VIEW IF EXISTS current_dept_emp;""",

    """CREATE VIEW current_dept_emp AS
        SELECT l.emp_no, d.dept_no, l.from_date, l.to_date
        FROM dept_emp d
        INNER JOIN dept_emp_latest_date l
        ON d.emp_no = l.emp_no AND d.from_date = l.from_date AND l.to_date = d.to_date;"""
]