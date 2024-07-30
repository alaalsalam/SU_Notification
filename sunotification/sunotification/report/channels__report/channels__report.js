// Copyright (c) 2024, sunotify and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Channels  Report"] = {
	filters: [
		// {
		// 	fieldname: "company",
		// 	label: __("Company"),
		// 	fieldtype: "Link",
		// 	options: "Company",
		// 	reqd: 1,
		// 	default: frappe.defaults.get_user_default("Company"),
		// },
		// {
		// 	fieldname: "department",
		// 	label: __("Department"),
		// 	fieldtype: "Link",
		// 	options: "Department",
		// 	reqd: 1,
		// 	default: frappe.defaults.get_user_default("Department"),
		// },
		{
			fieldname: "receiver",
			label: __("Receiver"),
			fieldtype: "Link",
			options: "User",
			
		},
		{
			fieldname: "sender",
			label: __("sender"),
			fieldtype: "Link",
			options: "User",
			
		},
		{
			fieldname: "post_date",
			label: __("Posting Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "send_type",
			label: __("Sent Type"),
			fieldtype: "Select",
			options: "\nEmail\nWhatsapp\nSystems Notification\nTelegram\nSMS",
		},
		// {
		// 	fieldname: "status",
		// 	label: __("Status"),
		// 	fieldtype: "Select",
		// 	options: "\nEmail\nWhatsapp\nSystem\nTelegram\nSMS",
		// },

		// {
		// 	fieldname: "enabled",
		// 	label: __("Enabled"),
		// 	fieldtype: "Check",
		// 	default: "1",

		// },
		// {
		// 	fieldname: "show_subject",
		// 	label: __("Show Subject"),
		// 	fieldtype: "Check",
		// },
		
	],
};
