from jinja2 import Environment, BaseLoader
from .report import Report
from .base_module import ModuleResult, BaseModule
from .default_modules import modules as default_modules




class Service:
    def __init__(self, template: str, additional_modules=[]) -> None:
        # template
        self.template = template
        self.environment = Environment(loader=BaseLoader())

        # modules
        self.additional_modules = additional_modules

        # to be generated and cleared automatically
        self.cached_data = {}
        self.module_log = []


    def _find_module(self, module_id) -> BaseModule:
        all_modules = default_modules + self.additional_modules
        for m in all_modules:
            if (m.module_id == module_id):
                return m


    def _fetch_module_result(self, module_id, **kwargs) -> ModuleResult:
        m = self._find_module(module_id)
        
        if (m):
            kwargs['cached_data'] = self.cached_data

            # initialize and get report results
            module = m(**kwargs)
            result = module.get_report_data()

            return result
    
    
    def _fetch_result_html(self, module_id, **kwargs) -> str:
        result = self._fetch_module_result(module_id, **kwargs)

        if (result and isinstance(result, ModuleResult)):
            self.module_log.append(result.text)
            return result.html
        return ''
        

    def _render_template(self) -> str:
        template = self.environment.from_string(self.template)
        content = template.render(module=self._fetch_result_html)
        return content


    def create_report(self, title) -> Report:
        content = self._render_template()

        log = self.module_log.copy()

        self.module_log.clear()
        self.cached_data.clear()

        return Report(title, content, log)