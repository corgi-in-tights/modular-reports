from modular_reports import ComponentService, Report, StringProvider, FileProvider
from datetime import datetime
from mjml import mjml_to_html
import os, json

from pathlib import Path

"""
1. Create a service - 
    service = Service(additional_components=[], developer_mode=False, global_data=[])
3. Pass in provider template to recieve HTML render - 
    service.render(provider, template, component_data=[])
4. Create report using helper method - 
    service.create_report(text_content, html_content) 
5. Send report via email using - 
    report.send_via_gmail()
"""

date = datetime.now().strftime("%A, %-d %b %Y")
service = ComponentService(
    template_kwargs={'date': date},
    global_component_kwargs={'sample-sentence': 'Hello, World!'},
    developer_mode=True
)
service.set_component_provider('base:quote', 'loco', StringProvider('hello world {{ date }}'))

text_content = service.render(template_provider=FileProvider(Path(__file__).parent / 'example/template'))
loco_content = service.render(FileProvider(Path(__file__).parent / 'example/template.txt'), 'loco')

mjml_content = service.render(FileProvider(Path(__file__).parent / 'example/example.mjml'), 'mjml')
html_content = mjml_to_html(mjml_content)

report = Report(f'Daily Report - {date}', text_content, html_content=html_content)

with open('./out.txt', 'w') as fp:
    fp.write(loco_content)
    