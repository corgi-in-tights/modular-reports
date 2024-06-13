from jinja2 import Environment, BaseLoader
from types import SimpleNamespace

from .report import Report
from .utils.file import get_file_content
from .components.weather import WeatherComponent
from .components.quote import QuoteComponent

environment = Environment(loader=BaseLoader())

default_components = [
    WeatherComponent,
    QuoteComponent      
]


class Service:
    def __init__(self, component_list, text_template_path, external_html_template=None, additional_components=[]) -> None:
        # template
        self.component_list = component_list
        self.text_template_path = text_template_path
        self.external_html_template = external_html_template
        self.environment = environment

        # components
        self.additional_components = additional_components

        # to be generated and cleared automatically
        self.cached_data = {}

    def get_component_class_by_type(self, _type):
        all_component_classes = self.additional_components + default_components
        for c in all_component_classes:
            if (c._type == _type):
                return c

    def generate_components(self, component_list):
        components = {}

        for c in component_list:
            _id = c['id']
            _type = c['component']
            _kwargs = c.get('kwargs', {})

            # idiot-proof the kwargs
            for k in _kwargs.keys():
                if (k in ['cached_data', 'environment']):
                    raise Exception('IDs cannot be reserved keywords `cached_data` or `environment`.')

            component = self.get_component_class_by_type(_type)
            if (component):
                # create instance and attach to id
                components[_id] = component(
                    environment=self.environment, cached_data=self.cached_data, **_kwargs
                )

        return components

    def render_template(self, template_content, provider, components):
        template = self.environment.from_string(template_content)
        
        rendered_components = {}
        for _id, c in components.items():
            print (f'Rendering {_id}')
            res = c.render(provider)
            if (res):
                rendered_components[_id] = res
            else:
                raise Exception(f'There was an error with component {_id}, no template was returned for provider {provider}.')

        # namespaced for template readability and reference
        # so you can refer to a component like so: `component.my_component_id`
        return template.render(component=SimpleNamespace(**rendered_components))

    def create_report(self, title) -> Report:
        # generate all required component instances
        components = self.generate_components(self.component_list)

        text_template_content = get_file_content(self.text_template_path)
        rendered_text_content = self.render_template(
            text_template_content, 'txt', components
        )

        rendered_html_content = None

        if (self.external_html_template):
            if (self.external_html_template['provider'] != 'html'):
                external_template_content = get_file_content(self.external_html_template['path'])
                rendered_external_content = self.render_template(external_template_content, self.external_html_template['provider'], components)

                if (self.external_html_template['converter']):
                    rendered_html_content = self.external_html_template['converter'](rendered_external_content)
                else:
                    rendered_html_content = rendered_external_content

            else:
                html_template_content = get_file_content(self.external_html_template['path'])
                rendered_html_content = self.render_template(
                    html_template_content, 'html', components
                )

        # reset cache
        self.cached_data.clear()

        return Report(title, text_content=rendered_text_content, html_content=rendered_html_content)
