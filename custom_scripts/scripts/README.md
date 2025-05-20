Run the following command to create the doctypes in your local database:

Install the required packages in a virtual environment:
```bash
source env/bin/activate
pip install pandas openpyxl
```
Add code to the `hooks.py` in custom_scripts file:
```
after_migrate = [
    "custom_scripts.scripts.create_doctypes.create_doctypes.execute_doctypes"
    ...
]
```
