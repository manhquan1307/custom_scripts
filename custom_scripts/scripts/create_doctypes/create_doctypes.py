import os
import pandas as pd
import frappe

def execute():
    wb_path = os.path.join(os.path.dirname(__file__), 'doctype_metadata.xlsx')
    if not os.path.exists(wb_path):
        print(f"ERROR: File not found: {wb_path}")
        return

    xls = pd.ExcelFile(wb_path)
    # Đọc permissions từ sheet 'Role'
    roles = []
    if 'Role' in xls.sheet_names:
        role_df = pd.read_excel(wb_path, 'Role')
        for _, r in role_df.iterrows():
            perm = {c: int(r.get(c, 0) or 0) for c in ['read','write','create','delete','submit','cancel','amend']}
            perm['role'] = r['role']
            perm['assign'] = perm['assign_submit'] = 0
            roles.append(perm)

    # Xử lý từng sheet (ngoại trừ Role)
    for sheet in xls.sheet_names:
        if sheet == 'Role':
            continue

        raw = pd.read_excel(wb_path, sheet, header=None)
        # tìm header 'fieldname'
        mask = raw.apply(lambda row: row.astype(str).str.lower().eq('fieldname').any(), axis=1)
        if not mask.any():
            print(f"SKIP {sheet}: no header")
            continue
        hdr_idx = mask.idxmax()

        # lấy metadata 2 dòng trên header (nếu có)
        meta_block = raw.iloc[:hdr_idx].dropna(axis=1, how='all')
        M = {}
        if len(meta_block) >= 2:
            keys = meta_block.iloc[-2].tolist()
            vals = meta_block.iloc[-1].tolist()
            M = {k: v for k, v in zip(keys, vals) if pd.notna(k) and pd.notna(v)}

        # chuẩn metadata với giá trị mặc định
        module = M.get('module', 'Custom Scripts')
        custom = int(M.get('custom', 1) or 1)
        is_tree = bool(int(M.get('is_tree', 0) or 0))
        parent_field = M.get('parent_field') if pd.notna(M.get('parent_field')) else None

        # tạo DataFrame fields
        df = raw.iloc[hdr_idx+1:].copy().reset_index(drop=True)
        df.columns = raw.iloc[hdr_idx].tolist()
        # loại bỏ dòng không có fieldname
        if 'fieldname' not in df.columns:
            print(f"SKIP {sheet}: missing 'fieldname' column")
            continue
        df = df[df['fieldname'].notna()]
        if df.empty:
            print(f"SKIP {sheet}: no fields")
            continue

        # ensure submit_table & child_table columns
        df['submit_table'] = df.get('submit_table', 0).fillna(0).astype(int)
        df['child_table'] = df.get('child_table', 0).fillna(0).astype(int)

        # chuẩn DocType spec
        first_field = df['fieldname'].iloc[0]
        if not frappe.db.exists('DocType', sheet):
            dt = frappe.new_doc('DocType')
            dt.name = sheet
            dt.module = module
            dt.custom = custom
        else:
            dt = frappe.get_doc('DocType', sheet)
            dt.fields = []
            dt.permissions = []

        dt.autoname = f'field:{first_field}'
        dt.is_tree = is_tree
        dt.parent_field = parent_field

        # thêm fields vào DocType với sanitize NaN
        for _, row in df.iterrows():
            def get_str(col):
                v = row.get(col)
                return '' if pd.isna(v) else str(v)
            field_data = {
                'fieldname': get_str('fieldname'),
                'label': get_str('label'),
                'fieldtype': get_str('fieldtype'),
                'options': get_str('options'),
                'insert_after': get_str('insert_after'),
                'reqd': int(row.get('reqd', 0) or 0),
                'in_list_view': int(row.get('in_list_view', 0) or 0),
                'submit_table': int(row['submit_table']),
                'child_table': int(row['child_table'])
            }
            dt.append('fields', field_data)

        # thêm permissions
        for perm in roles:
            if (perm['submit'] or perm['assign_submit']) and not dt.is_submittable:
                perm['submit'] = perm['assign_submit'] = 0
            dt.append('permissions', perm)

        # lưu DocType
        if dt.is_new():
            dt.insert()
        else:
            dt.save(ignore_permissions=True)
        frappe.db.commit()
        print(f"SYNCED {sheet}")

