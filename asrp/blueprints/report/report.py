from flask import Blueprint, jsonify
from .models import Report, ExtractionRequest, CrimeReport, IncidentReport, GroupReport
from .extensions import db

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports', methods=['GET'])
def get_reports():
    reports = Report.query.all()
    reports_data = []

    for report in reports:
        cr = report.crime_report
        ir = report.incident_report
        gr = report.group_report
        er = report.extraction_request

        report_data = {
            "id": report.id,
            "user_id": report.user_id,
            "region_id": report.region_id,
            "specific_address": report.specific_address,
            "created_at": report.created_at.isoformat(),
            "status_id": report.status_id,
            "category_id": report.category_id,

            "crime_report": {
                "case_code":            cr.case_code,
                "received_date":        cr.received_date.isoformat() if cr and cr.received_date else None,
                "officer_name":         cr.officer_name,
                "title":                cr.title,
                "content":              cr.content,
                "informant_name":       cr.informant_name,
                "informant_address":    cr.informant_address,
                "informant_phone":      cr.informant_phone,
                "status":               cr.status,
                "phone_numbers":        cr.phone_numbers,
                "bank_accounts":        cr.bank_accounts,
                "ip_addresses":         cr.ip_addresses,
                "websites_or_apps":     cr.websites_or_apps,
            } if cr else None,

            "incident_report": {
                "file_number":      ir.file_number,
                "incident_time":    ir.incident_time.isoformat() if ir and ir.incident_time else None,
                "incident_name":    ir.incident_name,
                "description":      ir.description,
                "officer_name":     ir.officer_name,
                "status":           ir.status,
                "related_persons":  ir.related_persons,
                "storage_number":   ir.storage_number,
                "archived_date":    ir.archived_date.isoformat() if ir and ir.archived_date else None,
            } if ir else None,

            "group_report": {
                "platform":           gr.platform,
                "group_name":         gr.group_name,
                "group_url":          gr.group_url,
                "created_at":         gr.created_at.isoformat() if gr and gr.created_at else None,
                "admin_info":         gr.admin_info,
                "member_count":       gr.member_count,
                "weekly_post_count":  gr.weekly_post_count,
                "status":             gr.status,
                "assigned_officer":   gr.assigned_officer,
                "purpose":            gr.purpose,
                "description":        gr.description,
                "note":               gr.note,
            } if gr else None,

            "extraction_request": {
                "request_number":     er.request_number,
                "sent_date":          er.sent_date.isoformat() if er and er.sent_date else None,
                "result_date":        er.result_date.isoformat() if er and er.result_date else None,
                "requester_id":       er.requester_id,
                "unit_id":            er.unit_id,
                "device_type":        er.device_type,
                "device_info":        er.device_info,
                "extraction_detail":  er.extraction_detail,
                "extraction_result":  er.extraction_result,
                "status":             er.status,
                "receiving_officer":  er.receiving_officer,
                "note":               er.note,
            } if er else None,
        }

        reports_data.append(report_data)

    return jsonify(reports_data)
