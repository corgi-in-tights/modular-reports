from modular_reports import ComponentService, FileProvider
from pathlib import Path
from .hello_world import HelloWorldComponent

service = ComponentService(additional_component_classes=[HelloWorldComponent])
# if we wanted to add another provider dynamically
# service.set_component_provider(
#     'mynamespace:hello_world', 
#     'loco', 
#     FileProvider(Path(__file__).parent / 'hello_world/hello_world.loco')
# )

content = service.render(FileProvider(Path(__file__).parent / 'template.txt'))

print (content)