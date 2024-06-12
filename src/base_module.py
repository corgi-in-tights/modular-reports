class ModuleResult:
    def __init__(self, html, text) -> None:
        self.html = html
        self.text = text


class BaseModule:
    module_id = None
    
    def __init__(self, cached_data, **kwargs) -> None:
        self.cached_data = cached_data

    def get_report_data(self) -> ModuleResult:
        pass