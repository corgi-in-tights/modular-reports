from modular_reports import Service
from datetime import datetime
from mjml import mjml_to_html
import os, json


with open('templates/weekday/components.json', 'r') as fp:
    component_list = json.load(fp)

text_template_path = 'templates/weekday/template.txt'
external_html_template = {
    'path': 'templates/weekday/template.mjml',
    'provider': 'mjml',
    'converter': lambda content: mjml_to_html(content).html
}

service = Service(component_list, text_template_path, external_html_template=external_html_template)
report = service.create_report(f'Daily Report - {datetime.now().strftime("%A, %-d %b %Y")}')

with open('out.html', 'w') as fp:
    fp.write(report.html_content)
    
# report.send_via_gmail('corgi.in.tights@gmail.com', 'chitale.reyaan@gmail.com', os.getenv('APP_PASSWORD'))
