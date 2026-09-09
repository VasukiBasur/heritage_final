import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
c=mysql.connector.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_NAME'))
cr=c.cursor(dictionary=True)

try:
    cr.execute("SELECT DATE_FORMAT(start_date, '%b %Y') as month, COUNT(log_id) as volume FROM production_logs WHERE start_date IS NOT NULL GROUP BY month ORDER BY MIN(start_date) ASC LIMIT 6")
    print("Trend:", cr.fetchall())
except Exception as e:
    print("Trend Error:", e)

try:
    cr.execute("SELECT a.name, COUNT(p.log_id) as total_logs, SUM(p.payout_amount) as total_payout FROM artisans a JOIN production_logs p ON a.artisan_id = p.artisan_id GROUP BY a.artisan_id, a.name ORDER BY total_logs DESC LIMIT 5")
    print("Artisan:", cr.fetchall())
except Exception as e:
    print("Artisan Error:", e)

try:
    cr.execute("SELECT status, COUNT(log_id) as count FROM production_logs GROUP BY status")
    print("Status:", cr.fetchall())
except Exception as e:
    print("Status Error:", e)
