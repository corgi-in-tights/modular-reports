from modular_reports import ComponentService, FileProvider, Report
from datetime import datetime
from pathlib import Path

from mjml import mjml_to_html


date = datetime.now().strftime("%A, %-d %b %Y")
service = ComponentService(
    template_kwargs={'date': date},
    global_component_kwargs={'sample-sentence': 'Hello, World!'},
    developer_mode=True
)

# mjml is a HTML framework which simplifies the email-making process by a fair bit
# this library supports any framework that uses a text-based format
mjml_content = service.render(template_provider=FileProvider(Path(__file__).parent / 'template.mjml'), default_component_provider_key='mjml')

# to send emails, however, only plain text or HTML are allowed
html_content = mjml_to_html(mjml_content)

print (html_content)