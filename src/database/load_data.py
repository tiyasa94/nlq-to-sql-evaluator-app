
from database.tables.load_departments import DEPARTMENT_DATA
from database.tables.load_dept_emp import DEPT_EMP_DATA
from database.tables.load_dept_manager import DEPT_MNG_DATA
from database.tables.load_employees import EMPLOYEES_DATA
from database.tables.load_salaries1 import SALARY_DATA_1
from database.tables.load_salaries2 import SALARY_DATA_2
from database.tables.load_salaries3 import SALARY_DATA_3
from database.tables.load_titles import TITLE_DATA



LOAD_DATA_QUERIES = [
            DEPARTMENT_DATA,
             DEPT_EMP_DATA,  
             DEPT_MNG_DATA,
             EMPLOYEES_DATA,
             SALARY_DATA_1,
             SALARY_DATA_2,
             SALARY_DATA_3,
             TITLE_DATA]