# Copyright (c) 2024, sunotify and contributors
# For license information, please see license.txt


# Copyright (c) 2024, Frappe Technologies and contributors
# For license information, please see license.txt

# scheduler = Scheduler('foo', connection=Redis()) # Get a scheduler for the "foo" queue
# queue = Queue('bar', connection=Redis())
# scheduler.enqueue_at(datetime(2024, 6, 2, 6), fun) # Date time should be in UTC
	
	# scheduler = Scheduler('foo', connection=Redis()) # Get a scheduler for the "foo" queue
		

	# 	queue = Queue('bar', connection=Redis())
	#     /scheduler.enqueue_at(datetime(2024, 6, 2, ), fun) # Date time should be in UTC
		
		
	# 	You can also instantiate a Scheduler using an RQ Queue
	# 	queue = Queue('bar', connection=Redis())
	# 	scheduler = Scheduler(queue=queue, connection=queue.connection)

	# 	Puts a job into the scheduler. The API is similar to RQ except that it
	# 	takes a datetime object as first argument. So for example to schedule a
	# 	job to run on Jan 1st 2020 we do:
	# 	scheduler.enqueue_at(datetime(2024, 5, 30, ), func) # Date time should be in UTC

	# 	Here's another example scheduling a job to run at a specific date and time (in UTC),
	# 	complete with args and kwargs.
	# 	scheduler.enqueue_at(datetime(2024, 5, 30, 12, 30), self.send())

	# 	You can choose the queue type where jobs will be enqueued by passing the name of the type to the scheduler
	# 	used to enqueue
	# 	scheduler = Scheduler('foo', queue_class="rq.Queue")
	# 	scheduler.enqueue_at(datetime(2024, 5, 30, 45), self.send()) # The job will be enqueued at the queue named "foo" using the queue type "rq.Queue"

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime

import json
import os

import frappe
from frappe import _
from frappe.core.doctype.role.role import get_info_based_on_role, get_user_info
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification
from frappe.integrations.doctype.slack_webhook_url.slack_webhook_url import send_slack_message
from frappe.model.document import Document
from frappe.modules.utils import export_module_json, get_doc_module
from frappe.utils import add_to_date, cast, is_html, nowdate, validate_email_address
from frappe.utils.jinja import validate_template
from frappe.utils.safe_exec import get_safe_globals

class SU_Notification(Document):
	def validate(self):

		
		if(self.when_to_send == "Scheduler"):
			frappe.msgprint("Scheduler.........")	
			# self.schedulingDate()
		if(self.when_to_send == "Now"):
			frappe.msgprint("Now.........^_^")
			self.send()	
		if(self.when_to_send == "Event"):
			frappe.msgprint("Event.........^_^")
			# self.sendevent()	
		if(self.when_to_send == "Recurring"):
			frappe.msgprint("Recurring......^_^")
			self.scheduling()		

	def sendevent(self):
					frappe.msgprint("Event ???????")
				
					notification = frappe.new_doc("Notification")
					notification.name = self.name
					notification.subject = self.subject
					notification.event = self.send_alert_on
					notification.document_type = self.document_type
					notification.channel = "System Notification"
					notification.recipients = self.recipients
					notification.enabled = self.enabled
					# notification.is_standard = self.is_standard
					notification.insert()
					frappe.msgprint("done save EVENT")


	def autoname(self):
		if not self.name:
			self.name = self.subject
	def schedulingDate(self):
		def sending():
			self.send()
		scheduler = Scheduler(connection=Redis()) # Get a scheduler for the "default" queue
		# scheduler = Scheduler('foo', connection=Redis()) # Get a scheduler for the "foo" queue

		# queue = Queue('bar', connection=Redis())
		# scheduler = Scheduler(queue=queue, connection=queue.connection)

		frappe.msgprint("scheduling......")
		# scheduler = Scheduler('foo', queue_class="rq.Queue")
		scheduler.enqueue_at(datetime(2024, 6, 2, 7, 21), self.send) # Date time should be in UTC

		# scheduler = Scheduler(connection=Redis()) # Get a scheduler for the "default" queue
		# scheduler.enqueue_at(datetime(2024, 6, 2, 6, 20), self.send) # Date time should be in UTC
		frappe.msgprint("scheduler after 	")
	def send(self):
		
		
		"""Build recipients and send Notification"""
		# doc = frappe.get_doc("Address", "A-Billing")
		doc = frappe.get_doc({
			'doctype': 'Message',
			'message':self.message
			})
		doc.insert()
		context = get_context(doc)
		context = {"doc": doc, "alert": self, "comments": None}
		if doc.get("_comments"):
			context["comments"] = json.loads(doc.get("_comments"))

		try:
			
			if self.system :
				frappe.msgprint("Sendigm Notification")
				self.create_system_notification(doc, context)

			if self.email :
				frappe.msgprint("send email ok ????")
				self.send_an_email(doc, context)


			if self.telegram :
				frappe.msgprint("send telegram..........")
				self.send_telegram(doc)

			if self.whatsapp :
				frappe.msgprint("send whatsapp..........")
				self.send_whatsapp()
				


		except Exception:
			self.log_error("Failed to send Notification")

	
	def scheduling(self):

		code2=f"""
doc = frappe.get_doc("SU_Notification","{self.name}")
doc.send()
			"""
		
		if self.event_frequency=="Cron":
			doc = frappe.get_doc({
				'doctype': 'Server Script',
				'name':self.subject,
		    	'script_type':'Scheduler Event',
		    	'cron_format': self.cron_format, 
		    	'event_frequency': self.event_frequency, 
		    	'script':code2
				})
			doc.insert()
		else:
			doc = frappe.get_doc({
				'doctype': 'Server Script',
				'name':self.subject,
		    	'script_type':'Scheduler Event', 
		  	  	'event_frequency': self.event_frequency, 
		    	'script':code2
				})
			doc.insert()


	def create_system_notification(self, doc, context):
		subject = self.subject
		if "{" in subject:
			subject = frappe.render_template(self.subject, context)

		attachments = self.get_attachment(doc)

		# users = ["mustafaalyemeni39@gmail.com","admin@example.com"]
		users = []
		# recipients, cc, bcc = self.get_list_of_recipients(doc, context)
		for recipient in self.recipients:
			# frappe.msgprint(recipient.email)
			users.append(recipient.email)

		if not users:
			return

		notification_doc = {
			"type": "Alert",
			"document_type": doc.doctype,
			"document_name": doc.name,
			"subject": subject,
			"from_user": doc.modified_by or doc.owner,
			"email_content": frappe.render_template(self.message, context),
			"attached_file": attachments and json.dumps(attachments[0]),
		}
		enqueue_create_notification(users, notification_doc)

	def send_an_email(self, doc, context):
	

		from email.utils import formataddr

		from frappe.core.doctype.communication.email import _make as make_communication

		subject = self.subject
		if "{" in subject:
			subject = frappe.render_template(self.subject, context)
		attachments = self.get_attachment(doc)
		# userss, cc, bcc = self.get_list_of_recipients(doc, context)
		# frappe.msgprint("userss userss .........")

		userss = []
		# recipients, cc, bcc = self.get_list_of_recipients(doc, context)
		for recipient in self.recipients:
			userss.append(recipient.email)

		if not (userss):
			return

		sender = None
		message = frappe.render_template(self.message, context)
		if self.sender and self.sender_email:
			sender = formataddr((self.sender, self.sender_email))
		frappe.sendmail(
			recipients=userss,
			subject=subject,
			sender=sender,
			# cc=cc,
			# bcc=bcc,
			message=message,
			reference_doctype=doc.doctype,
			reference_name=doc.name,
			attachments=attachments,
			expose_recipients="header",
			print_letterhead=((attachments and attachments[0].get("print_letterhead")) or False),
		)

		# Add mail notification to communication list
		# No need to add if it is already a communication.
		if doc.doctype != "Communication":
			make_communication(
				doctype=doc.doctype,
				name=doc.name,
				content=message,
				subject=subject,
				sender=sender,
				recipients=userss,
				communication_medium="Email",
				send_email=False,
				attachments=attachments,
				# cc=cc,
				# bcc=bcc,
				communication_type="Automated Message",
			)

    




	def send_telegram(self, doc):
		# for number in self.numbers_of_recipients:
		frappe.msgprint("xxxxxxxxxxxxxxxxx")
		doc = frappe.get_doc({
			'doctype':'Telegram Notification',
			'subject':self.subject,
		    'message': self.message,
			'document_type': doc,
		    'telegram_chat_id':self.telegram_chat_id,
			'channel':"Telegram",
			'evevt':self.event,
				})
		doc.insert()
		frappe.msgprint("Doneeeeeeeeeeeeee")


	def send_whatsapp(self):
		frappe.msgprint("aaaaaaaaaa send_whatsapp send_whatsapp .........")

		numbers = []
		for recipient in self.recipients:
			numbers.append(recipient.mobile)
			doc = frappe.get_doc({
			'doctype':'WhatsApp Message',
			'label':self.subject,
			'name':recipient.mobile, 
		    'to': "+967777433779", 
		    'message': self.message,
		    'content_type':'text'
			})
			doc.insert()





	def get_list_of_recipients(self, doc, context):
		recipients = []
		cc = []
		bcc = []
		for recipient in self.recipients:
			if recipient.condition:
				if not frappe.safe_eval(recipient.condition, None, context):
					continue
			if recipient.receiver_by_document_field:
				fields = recipient.receiver_by_document_field.split(",")
				# fields from child table
				if len(fields) > 1:
					for d in doc.get(fields[1]):
						email_id = d.get(fields[0])
						if validate_email_address(email_id):
							recipients.append(email_id)
				# field from parent doc
				else:
					email_ids_value = doc.get(fields[0])
					if validate_email_address(email_ids_value):
						email_ids = email_ids_value.replace(",", "\n")
						recipients = recipients + email_ids.split("\n")

			cc.extend(get_emails_from_template(recipient.cc, context))
			bcc.extend(get_emails_from_template(recipient.bcc, context))

			# For sending emails to specified role
			if recipient.receiver_by_role:
				emails = get_info_based_on_role(recipient.receiver_by_role, "email", ignore_permissions=True)

				for email in emails:
					frappe.msgprint(email.split("\n")[0])
					recipients = recipients + email.split("\n")

		return list(set(recipients)), list(set(cc)), list(set(bcc))

	def get_receiver_list(self, doc, context):
		"""return receiver list based on the doc field and role specified"""
		receiver_list = []
		for recipient in self.recipients:
			if recipient.condition:
				if not frappe.safe_eval(recipient.condition, None, context):
					continue

			# For sending messages to the owner's mobile phone number
			if recipient.receiver_by_document_field == "owner":
				receiver_list += get_user_info([dict(user_name=doc.get("owner"))], "mobile_no")
			# For sending messages to the number specified in the receiver field
			elif recipient.receiver_by_document_field:
				receiver_list.append(doc.get(recipient.receiver_by_document_field))

			# For sending messages to specified role
			if recipient.receiver_by_role:
				receiver_list += get_info_based_on_role(recipient.receiver_by_role, "mobile_no")

		return receiver_list

	def get_attachment(self, doc):
		"""check print settings are attach the pdf"""
		if not self.attach_print:
			return None

		print_settings = frappe.get_doc("Print Settings", "Print Settings")
		if (doc.docstatus == 0 and not print_settings.allow_print_for_draft) or (
			doc.docstatus == 2 and not print_settings.allow_print_for_cancelled
		):

			# ignoring attachment as draft and cancelled documents are not allowed to print
			status = "Draft" if doc.docstatus == 0 else "Cancelled"
			frappe.throw(
				_(
					"""Not allowed to attach {0} document, please enable Allow Print For {0} in Print Settings"""
				).format(status),
				title=_("Error in Notification"),
			)
		else:
			return [
				{
					"print_format_attachment": 1,
					"doctype": doc.doctype,
					"name": doc.name,
					"print_format": self.print_format,
					"print_letterhead": print_settings.with_letterhead,
					"lang": frappe.db.get_value("Print Format", self.print_format, "default_print_language")
					if self.print_format
					else "en",
				}
			]

	# def on_trash(self):
	# 	frappe.cache().hdel("notifications", self.document_type)


def get_context(doc):
	return {
		"doc": doc,
		"nowdate": nowdate,
		"frappe": frappe._dict(utils=get_safe_globals().get("frappe").get("utils")),
	}



def get_emails_from_template(template, context):
	if not template:
		return ()

	emails = frappe.render_template(template, context) if "{" in template else template
	return filter(None, emails.replace(",", "\n").split("\n"))
