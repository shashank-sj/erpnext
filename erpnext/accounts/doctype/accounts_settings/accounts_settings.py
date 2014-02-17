# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cint

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		frappe.conn.set_default("auto_accounting_for_stock", self.doc.auto_accounting_for_stock)
		
		if cint(self.doc.auto_accounting_for_stock):
			# set default perpetual account in company
			for company in frappe.conn.sql("select name from tabCompany"):
				frappe.bean("Company", company[0]).save()
			
			# Create account head for warehouses
			warehouse_list = frappe.conn.sql("select name, company from tabWarehouse", as_dict=1)
			warehouse_with_no_company = [d.name for d in warehouse_list if not d.company]
			if warehouse_with_no_company:
				frappe.throw(_("Company is missing in following warehouses") + ": \n" + 
					"\n".join(warehouse_with_no_company))
			for wh in warehouse_list:
				wh_bean = frappe.bean("Warehouse", wh.name)
				wh_bean.save()