import re

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_routes = """@app.route('/supplier/schedule/api/new', methods=['POST'])
@login_required
def create_supplier_schedule():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.json
    hub = data.get('hub')
    date = data.get('date')
    time = data.get('time')
    fleet = data.get('fleet')
    
    if not all([hub, date, time, fleet]):
        return jsonify({'success': False, 'message': 'Missing fields'}), 400
        
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO supplier_dispatches (hub_name, dispatch_date, dispatch_time, fleet_assigned) VALUES (%s, %s, %s, %s)",
                (hub, date, time, fleet)
            )
            conn.commit()
            dispatch_id = cursor.lastrowid
            return jsonify({'success': True, 'id': dispatch_id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'success': False, 'message': 'Database connection failed'}), 500

@app.route('/supplier/schedule/api/list', methods=['GET'])
@login_required
def list_supplier_schedules():
    if session.get('role') != 'Supplier' and session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM supplier_dispatches ORDER BY dispatch_date, dispatch_time")
            schedules = cursor.fetchall()
            
            for s in schedules:
                if s.get('dispatch_date'):
                    s['dispatch_date'] = s['dispatch_date'].strftime('%Y-%m-%d')
                if s.get('created_at'):
                    s['created_at'] = s['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                    
            return jsonify({'success': True, 'data': schedules})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'success': False, 'message': 'Database connection failed'}), 500

if __name__ == '__main__':
"""

clean_text = re.sub(r'@app\.route\(\'/supplier/schedule/api/new\'.*?if __name__ == \'__main__\':\n', new_routes, text, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(clean_text)

print('Cleaned up app.py completely.')
