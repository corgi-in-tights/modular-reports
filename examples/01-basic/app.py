from modular_reports import ComponentService, FileProvider
from datetime import datetime
from pathlib import Path


date = datetime.now().strftime("%A, %-d %b %Y")
service = ComponentService(
    template_kwargs={'date': date},
    global_component_kwargs={'sample-sentence': 'Hello, World!'},
    developer_mode=True
)

content = service.render(template_provider=FileProvider(Path(__file__).parent / 'template.txt'))

print (content)