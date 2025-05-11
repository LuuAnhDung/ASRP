from flask import Blueprint, jsonify
from .models import Report, ExtractionRequest, CrimeReport, IncidentReport, GroupReport
from .extensions import db

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/reports', methods=['GET'])
def get_reports():
    # Lấy tất cả các báo cáo từ bảng Report
    reports = Report.query.all()
    
    reports_data = []
    
    for report in reports:
        # Lấy các thông tin liên quan đến các báo cáo con
        crime_report = report.crime_report
        incident_report = report.incident_report
        group_report = report.group_report
        extraction_request = report.extraction_request
        
        report_data = {
            "id": report.id,
            "user_id": report.user_id,
            "region_id": report.region_id,
            "specific_address": report.specific_address,
            "created_at": report.created_at,
            "status_id": report.status_id,
            "category_id": report.category_id,
            "crime_report": {
                "title": crime_report.title if crime_report else None,
                "content": crime_report.content if crime_report else None,
                "informant_name": crime_report.informant_name if crime_report else None,
                "informant_address": crime_report.informant_address if crime_report else None,
                "informant_phone": crime_report.informant_phone if crime_report else None,
                "informant_id_number": crime_report.informant_id_number if crime_report else None,
            },
            "incident_report": {
                "incident_name": incident_report.incident_name if incident_report else None,
                "description": incident_report.description if incident_report else None,
                "occurred_at": incident_report.occurred_at if incident_report else None,
                "related_people": incident_report.related_people if incident_report else None,
            },
            "group_report": {
                "platform": group_report.platform if group_report else None,
                "group_name": group_report.group_name if group_report else None,
                "group_url": group_report.group_url if group_report else None,
                "created_at": group_report.created_at if group_report else None,
                "admin_info": group_report.admin_info if group_report else None,
                "purpose": group_report.purpose if group_report else None,
                "impact_level": group_report.impact_level if group_report else None,
                "description": group_report.description if group_report else None,
                "note": group_report.note if group_report else None,
            },
            "extraction_request": {
                "request_number": extraction_request.request_number if extraction_request else None,
                "requester_id": extraction_request.requester_id if extraction_request else None,
                "unit_id": extraction_request.unit_id if extraction_request else None,
                "result_date": extraction_request.result_date if extraction_request else None,
                "device_type": extraction_request.device_type if extraction_request else None,
                "device_info": extraction_request.device_info if extraction_request else None,
                "extraction_detail": extraction_request.extraction_detail if extraction_request else None,
                "extraction_result": extraction_request.extraction_result if extraction_request else None,
                "note": extraction_request.note if extraction_request else None,
            }
        }
        
        reports_data.append(report_data)
    
    return jsonify(reports_data)
