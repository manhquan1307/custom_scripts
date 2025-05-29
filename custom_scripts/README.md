# Custom Scripts for Frappe Setup

This app contains automation scripts for initializing your Frappe project, including custom DocType creation, role cleanup, permission imports, and role restrictions.

---

## 1. 🛠️ Script Setup

### 1.1 Install Required Python Packages

Activate your virtual environment and install required dependencies:

```bash
    source env/bin/activate
    pip install pandas openpyxl
```

---

### 1.2 Folder Structure

```
scripts/
├── create_doctypes/
│   ├── create_doctypes.py            # Create DocTypes from Excel
│   ├── doctype_metadata.xlsx         # Excel file with DocType metadata
│
├── delete_and_disable_roles/
│   ├── delete_and_disable_roles.py   # Remove or disable default roles
│
├── import_permissions/
│   ├── import_permissions.py         # Import permissions from Excel
│   ├── Role Permissions Manager.xlsx # Excel mapping for permissions
│
└── __init__.py                       # Init module marker
```

---

### 1.3 Register Scripts in `hooks.py`

Add the following to your `custom_scripts/hooks.py`:

```python
after_migrate = [
    "custom_scripts.scripts.delete_and_disable_roles.delete_and_disable_roles.execute",
    "custom_scripts.scripts.import_permissions.import_permissions.execute",
    # Optional: Run create_doctypes manually via bench execute
]
```

---

## 2. 🔒 Hide Reserved Roles in Role List

Hide roles like **System Manager** and **Administrator** from the Role List for non-admin users.

### 2.1 Python Override

**File:** `custom_scripts/overrides/filter_role_list.py`

### 2.2 Add to `hooks.py`

```python
override_whitelisted_methods = {
    "frappe.desk.reportview.get": "custom_scripts.overrides.filter_role_list.custom_get"
}
```

---

## 3. 🚫 Block Reserved Role Creation

Prevent users from creating reserved roles such as **System Manager** and **Administrator**.

### 3.1 Server-side Validation

**File:** `custom_scripts/overrides/role.py`
Overrides Role Doctype to block creation of reserved names.

### 3.2 Client-side Validation

**File:** `custom_scripts/public/js/role.js`
Adds UI validation to prevent input of reserved role names.

### 3.3 Add to `hooks.py`

```python
doctype_js = {
    "Role": "public/js/role.js"
}

override_doctype_class = {
    "Role": "custom_scripts.overrides.role.Role"
}
```

## 4. 🔐 Overrides 403 Error

This setup customizes the default 403 PermissionError in Frappe and returns HTTP 404 instead when users access restricted resources.

### 4.1 Copy permission functions

- Create a new function `custom_has_permission` copied from `frappe.permissions.has_permission`
- Create a new function `custom_init_has_permission` copied from `frappe.has_permission` in `frappe.__init__`
- Customize these functions to handle permission logging and message display as required

### 4.2 Custom Logging or Response Handling

You can update the log messages or return behavior in these new functions to better suit your system’s UX (for example, display "Not Found" instead of "Not Permitted").

### 4.3 Register overrides in `custom_scripts/__init__.py`

```python
import frappe
from custom_scripts.overrides import overrides_403_err
import frappe.exceptions

frappe.exceptions.PermissionError.http_status_code = 404
frappe.permissions.has_permission = overrides_403_err.custom_has_permission
frappe.has_permission = overrides_403_err.custom_init_has_permission
```
