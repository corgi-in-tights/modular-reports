from ..base_module import BaseModule, ModuleResult


class TitleModule(BaseModule):
    module_id = 'title'
    
    def __init__(self, name, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name

    def get_report_data(self):
        return ModuleResult('Hello ' + self.name, 'hi')