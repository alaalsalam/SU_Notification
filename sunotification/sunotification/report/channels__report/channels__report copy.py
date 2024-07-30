# Copyright (c) 2023, alaalsalam and contributors
# For license information, please see license.txt


import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data


def get_columns():
	columns = [
		{
			"label": _("Vin"),
			"fieldname": "vin",
			"fieldtype": "Link",
			"options": "Customer Vehicles",
			"width": 150,
		},
		{
			"fieldname": "customer",
			"label": _("customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 100,
		},
		{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 120},
		{"label": _("Container No"), "fieldname": "container_no", "fieldtype": "Data", "width": 120},
		{"label": _("Batch"), "fieldname": "batch", "fieldtype": "Data", "width": 120},
  
		{"label": _("Buying Towing"), "fieldname": "buying_towing", "fieldtype": "Data", "width": 120},
		{"label": _("Selling Towing"), "fieldname": "selling_towing", "fieldtype": "Data", "width": 120},
		{"label": _("Gross Profit Towing"), "fieldname": "gross_profit_towing", "fieldtype": "Data", "width": 120},
	
		{"label": _("Ocean Freight Price"), "fieldname": "buying_ocean_freight", "fieldtype": "Data", "width": 120},
		{"label": _("Selling Ocean Freight"), "fieldname": "selling_ocean_freight", "fieldtype": "Data", "width": 120},
		{"label": _("Gross Profit Ocean"), "fieldname": "gross_profit_ocean", "fieldtype": "Data", "width": 120},
  
  		{"label": _("Buying Transit"), "fieldname": "buying_transit", "fieldtype": "Data", "width": 120},
		{"label": _("Selling Transit"), "fieldname": "selling_transit", "fieldtype": "Data", "width": 120},
		{"label": _("Gross Profit Transit"), "fieldname": "gross_profit_transit", "fieldtype": "Data", "width": 120},
	]
	return columns


def get_data(filters):
    return frappe.db.sql(
        """
        SELECT
            `tabGL Shipping`.name as vin,
            `tabGL Shipping`.customer,
            `tabGL Shipping`.description,
            `tabGL Shipping`.container_no,
            `tabGL Shipping`.batch,
            `tabGL Shipping`.buying_towing,
            `tabGL Shipping`.selling_towing,
            `tabGL Shipping`.gross_profit_towing,
            `tabGL Shipping`.buying_ocean_freight,
            `tabGL Shipping`.selling_ocean_freight,
            `tabGL Shipping`.gross_profit_ocean,
            `tabGL Shipping`.buying_transit,
            `tabGL Shipping`.selling_transit,
            `tabGL Shipping`.gross_profit_transit
        FROM
            `tabGL Shipping`
        WHERE
            `tabGL Shipping`.name IS NOT NULL {conditions}
        ORDER BY
            `tabGL Shipping`.creation ASC """.format(
                conditions=get_conditions(filters)
            ),
        filters,
        as_dict=1,
    )


def get_conditions(filters):
	conditions = []

	if filters.get("vin"):
		conditions.append(" and `tabGL Shipping`.name=%(vin)s")

	if filters.get("customer"):
		conditions.append(" and `tabGL Shipping`.customer=%(customer)s")

	return " ".join(conditions) if conditions else ""
