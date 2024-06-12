from src import Service
from datetime import datetime
import os

with open('basic.html', 'r') as fp:
    template = fp.read()

service = Service(template)
report = service.create_report(f'Daily Report - {datetime.now().strftime("%A, %-d %b %Y")}')

report.send_via_gmail('corgi.in.tights@gmail.com', 'chitale.reyaan@gmail.com', os.getenv('APP_PASSWORD'))