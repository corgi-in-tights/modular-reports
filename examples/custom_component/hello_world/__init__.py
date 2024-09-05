from pathlib import Path

from modular_reports import BaseComponent
from modular_reports import FileProvider

class HelloWorldComponent(BaseComponent):
    component_id = 'mynamespace:hello_world'
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_default_provider(FileProvider(Path(__file__).parent / 'hello_world.txt'))
        # if we wanted to add our custom provider the recommended way
        # self.set_provider('loco', FileProvider(Path(__file__).parent / 'hello_world.loco'))


    def get_component_data(self, my_required_attribute, **kwargs):
        if (self.developer_mode): 
            return {
                'title': 'Developer mode on! Testing, testing!'
            }
        
        return {
            'title': f'You said this: {my_required_attribute}?'
        }