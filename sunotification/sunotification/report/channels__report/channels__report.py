# Copyright (c) 2024, sunotify and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns=[
		{
		"fieldname": "receiver",
		"fieldtype":"Data",
		"label":"Receiver",
		"width":150
		},
		{
		"fieldname": "status",
		"fieldtype":"Data",
		"label":"Status",
		"width":150
		},
		{
		"fieldname": "channel",
		"fieldtype":"Data",
		"label":"Channel",
		"width":150
		},
		
	]
	
	data=[]

	# Notification:
	notification_doc = frappe.get_all("Notification Log",fields=["for_user","read"],)
	notification_data=[]

	for notification in notification_doc:
		notification_data.append(
			{
				"receiver": notification["for_user"],
				"status":  "Read" if notification["read"]==1 else "Not Read",
				"channel": "Systems Notification"
				
			}
			
			)

	data = data + notification_data

	# Eemail:
	email_doc = frappe.get_all("Email Queue",fields=["recipients.recipient","recipients.status"],)
	email_data=[]

	for email in email_doc:
		email_data.append(
			{
				"receiver": email["recipient"],
				"status":  email["status"],
				"channel": "Email"
				
			}
			
			)

	data = data + email_data

	# Telegram:
	telegram_doc = frappe.get_all("Extra Notification Log",fields=["to_party","status"],)
	telegram_data=[]

	for telegram in telegram_doc:
		telegram_data.append(
			{
				"receiver": telegram["to_party"],
				"status":  telegram["status"],
				"channel": "Telegram"
				
			}
			
			)

	data = data + telegram_data

	# WhatsApp :
	whatsApp_doc = frappe.get_all("WhatsApp Message",fields=["to","status"],)
	whatsApp_data=[]

	for whatsApp in whatsApp_doc:
		whatsApp_data.append(
			{
				"receiver": whatsApp["to"],
				"status":  whatsApp["status"],
				"channel": "WhatsApp"
				
			}
			
			)

	data = data + whatsApp_data

	return columns, data