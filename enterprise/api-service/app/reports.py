from flask import jsonify
from app.auth import token_required
from app.models import Report

@token_required
def get_reports(current_user):
    try:
        reports = Report.query.filter_by(user_id=current_user.id).all()
        report_list = [{'id': report.id, 'title': report.title, 'content': report.content} for report in reports]
        return jsonify({'reports': report_list}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred while retrieving reports'}), 500