from jinja2 import Environment, BaseLoader

from .providers import Provider
from .base_component import BaseComponent
from .constants import default_component_classes, default_component_provider_key, jinja2_component_function

environment = Environment(loader=BaseLoader())

class ComponentService:
    def __init__(self, template_kwargs={}, global_component_kwargs={}, additional_component_classes=[], developer_mode=False) -> None:
        self.environment = environment 
        self.developer_mode = developer_mode
        if (self.developer_mode): print('Developer mode has been enabled.')

        # passed to template
        self.template_kwargs = template_kwargs

        # passed to template
        if (jinja2_component_function in global_component_kwargs): 
            raise Exception(f'`{jinja2_component_function}` is a reserved keyword!')
        self.global_component_kwargs = global_component_kwargs

        # resets after a finished render
        self.cached_data = {}

        # persists between renders
        self.persistent_data = {}

        
        # convert component classes into instances
        all_component_classes = additional_component_classes + default_component_classes 
        self.components = [
                component_class(
                    environment=self.environment,
                    cached_data=self.cached_data,
                    persistent_data=self.persistent_data,
                    developer_mode=self.developer_mode
                )
            for component_class in all_component_classes
        ]


    def get_component_by_id(self, component_id) -> BaseComponent:
        """Linear search to find component with matching id."""
        for c in self.components:
            if (c.component_id == component_id):
                return c
        raise KeyError(f'Could not find component by identifier: `{component_id}`')


    def set_component_provider(self, component_id: str, provider_id: str, provider: Provider) -> None:
        """Set or replace Provider for all component instances of the matching class."""
        for c in self.components:
            if (c.component_id == component_id):
                c.set_provider(provider_id, provider)


    def _render_component(self, component_id: str, component_provider: str = None, **component_kwargs):
        """
        Passed to Jinja2 as `component` to be used as a function
        """
        component = self.get_component_by_id(component_id)
        # use a provider specified by the template or the default one provided by render() 
        temporary_component_provider = self.temporary_component_provider if (component_provider == None) else component_provider

        provider = component.get_provider_by_key(temporary_component_provider)
        component_content = component.render(provider, **self.global_component_kwargs, **component_kwargs)
        return component_content


    def render(self, template_provider: Provider, default_component_provider_key = default_component_provider_key) -> str:
        """
        Accepts a Jinja2 template as Provider (use StringProvider if passing directly).
        `default_component_provider_key` used for component definitions inside template, for convenience.
        """
        # passed to _render_component()
        self.temporary_component_provider = default_component_provider_key

        source = template_provider.get_content()
        template = self.environment.from_string(source)
        content = template.render(component=self._render_component, **self.template_kwargs)

        # reset component providers and cached data
        self.cached_data = {}
        self.temporary_component_provider = default_component_provider_key

        return content