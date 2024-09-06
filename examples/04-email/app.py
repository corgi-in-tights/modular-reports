from modular_reports import ComponentService, FileProvider, Report
from datetime import datetime
from pathlib import Path


date = datetime.now().strftime("%A, %-d %b %Y")
service = ComponentService(
    template_kwargs={'date': date},
    global_component_kwargs={'sample-sentence': 'Hello, World!'},
    developer_mode=True
)

# best to use BOTH HTML and text, the report automatically compiles them
# into a multipart email where text is used instead of html when HTML is not ava. to render
# certain email clients may not be OK with HTML
text_content = service.render(template_provider=FileProvider(Path(__file__).parent / 'template.txt'))
html_content = service.render(template_provider=FileProvider(Path(__file__).parent / 'template.html'), default_component_provider_key='html')

report = Report('My Email Subject', text_content, html_content)

# ideally use environment variables
report.send_via_gmail('you@gmail.com', ['joe@gmail.com', 'bob@gmail.com'], 'myemailpassword')