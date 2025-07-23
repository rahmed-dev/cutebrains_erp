import frappe

def set_deduction_days(doc, method):
    deduction_days = 0

    # Fetch matching Days Deduction records
    deduction_docs = frappe.get_all(
        "Days Deduction",
        filters={
            "payroll_date": ["between", [doc.start_date, doc.end_date]],
            "docstatus": 1
        },
        fields=["name"]
    )

    for d in deduction_docs:
        if not d.name:
            continue

        try:
            parent_doc = frappe.get_doc("Days Deduction", d.name)
        except frappe.DoesNotExistError:
            frappe.msgprint(f"Days Deduction {d.name} not found")
            continue

        for row in parent_doc.details:
            if row.employee == doc.employee and row.deduction:
                deduction_days = row.deduction

    doc.custom_deduction_days = deduction_days