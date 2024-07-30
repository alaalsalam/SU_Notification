# Copyright (c) 2024, sunotify and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns, data = get_data(filters)
    return columns, data

def get_data(filters):
    query = """
        SELECT
            receiver,
            status,
            channel
        FROM (
            SELECT
                for_user AS receiver,
                CASE
                    WHEN `read`=1 THEN 'Read'
                    ELSE 'Not Read'
                END AS status,
                'Systems Notification' AS channel
            FROM
                `tabNotification Log`
            UNION ALL
            SELECT
                recipients.recipient AS receiver,
                recipients.status AS status,
                'Email' AS channel
            FROM
                `tabEmail Queue`
            INNER JOIN
                `tabEmail Queue Recipient` AS recipients
            ON
                `tabEmail Queue`.name = recipients.parent
            UNION ALL
            SELECT
                to_party AS receiver,
                status,
                'Telegram' AS channel
            FROM
                `tabExtra Notification Log`
            UNION ALL
            SELECT
                `to` AS receiver,
                status,
                'WhatsApp' AS channel
            FROM
                `tabWhatsApp Message`
        ) AS combined_data
        WHERE
            1=1 {conditions}
        ORDER BY
            receiver ASC
    """.format(
        conditions=get_conditions(filters)
    )
    
    data = frappe.db.sql(query, filters, as_dict=1)
    
    columns = [
        {"fieldname": "receiver", "label": "Receiver", "fieldtype": "Data", "width": 200},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 100},
        {"fieldname": "channel", "label": "Channel", "fieldtype": "Data", "width": 150},
    ]

    return columns, data

def get_conditions(filters):
    conditions = []
    if filters.get("receiver"):
        conditions.append(" AND receiver=%(receiver)s")
    if filters.get("status"):
        conditions.append(" AND status=%(status)s")
    if filters.get("channel"):
        conditions.append(" AND channel=%(channel)s")
    # if filters.get("company"):
        # conditions.append(" AND company=%(company)s")
    # if filters.get("department"):
    #     conditions.append(" AND department=%(department)s")
    # if filters.get("post_date"):
        # conditions.append(" AND DATE(post_date)=%(post_date)s")
    if filters.get("send_type"):
        conditions.append(" AND channel=%(send_type)s")
    # if filters.get("enabled"):
    #     conditions.append(" AND enabled=%(enabled)s")

    return " ".join(conditions) if conditions else ""


# def get_data(filters):
#     return frappe.db.sql(
#         """
#         SELECT
#             `tabNotification Log`.receiver as vin,
#             `tabNotification Log`.status,
#             `tabNotification Log`.for_user,
#             `tabNotification Log`.read,
#             `tabNotification Log`.channel
#         FROM
#             `tabNotification Log`
#         WHERE
#             `tabNotification Log`.name IS NOT NULL {conditions}
#         ORDER BY
#             `tabNotification Log`.creation ASC """.format(
#                 conditions=get_conditions(filters)
#             ),
#         filters,
#         as_dict=1,
#     )

# def get_conditions(filters):
# 	conditions = []

# 	if filters.get("vin"):
# 		conditions.append(" and `tabNotification Log`.name=%(vin)s")

# 	if filters.get("customer"):
# 		conditions.append(" and `tabNotification Log`.customer=%(customer)s")

# 	return " ".join(conditions) if conditions else ""


# def get_data(filters):

	# # Notification:
	# notification_doc = frappe.get_all("Notification Log",fields=["for_user","read"],)
	# notification_data=[]

	# for notification in notification_doc:
	# 	notification_data.append(
	# 		{
	# 			"receiver": notification["for_user"],
	# 			"status":  "Read" if notification["read"]==1 else "Not Read",
	# 			"channel": "Systems Notification"
				
	# 		}
			
	# 		)

	# data = data + notification_data

	# # Eemail:
	# email_doc = frappe.get_all("Email Queue",fields=["recipients.recipient","recipients.status"],)
	# email_data=[]

	# for email in email_doc:
	# 	email_data.append(
	# 		{
	# 			"receiver": email["recipient"],
	# 			"status":  email["status"],
	# 			"channel": "Email"
				
	# 		}
			
	# 		)

	# data = data + email_data

	# # Telegram:
	# telegram_doc = frappe.get_all("Extra Notification Log",fields=["to_party","status"],)
	# telegram_data=[]

	# for telegram in telegram_doc:
	# 	telegram_data.append(
	# 		{
	# 			"receiver": telegram["to_party"],
	# 			"status":  telegram["status"],
	# 			"channel": "Telegram"
				
	# 		}
			
	# 		)

	# data = data + telegram_data

	# # WhatsApp :
	# whatsApp_doc = frappe.get_all("WhatsApp Message",fields=["to","status"],)
	# whatsApp_data=[]

	# for whatsApp in whatsApp_doc:
	# 	whatsApp_data.append(
	# 		{
	# 			"receiver": whatsApp["to"],
	# 			"status":  whatsApp["status"],
	# 			"channel": "WhatsApp"
				
	# 		}
			
	# 		)

	# data = data + whatsApp_data

	# return columns, data