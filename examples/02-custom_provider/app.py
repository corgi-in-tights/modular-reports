from modular_reports import ComponentService, StringProvider, FileProvider
from pathlib import Path

service = ComponentService()
service.set_component_provider('base:quote', 'loco', StringProvider('This is the `loco` provider quote!'))
service.set_component_provider('base:weather', 'loco', FileProvider(Path(__file__).parent / 'weather.loco'))

content = service.render(
    template_provider=FileProvider(Path(__file__).parent / 'template.txt'), 
    default_component_provider_key='loco'
)

print (content)