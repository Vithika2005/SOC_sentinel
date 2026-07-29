from flask import request, jsonify
from app.auth import token_required
from app.database import init_db, db
from app.models import Report  # Assuming you have a Report model defined

app = Flask(__name__)
app.config.from_object(app_config['development'])
init_db(app)

@app.route('/reports', methods=['GET'])
@token_required
def get_reports(current_user):
    try:
        # Retrieve reports for the current user
        reports = Report.query.filter_by(user_id=current_user.id).all()
        
        # Convert reports to a list of dictionaries
        report_list = [{'id': report.id, 'title': report.title, 'content': report.content} for report in reports]
        
        return jsonify({'reports': report_list}), 200
    except Exception as e:
        app.logger.error(f"Error retrieving reports: {e}")
        return jsonify({'message': 'An error occurred while retrieving reports'}), 500

if __name__ == '__main__':
    app.run(debug=True)
