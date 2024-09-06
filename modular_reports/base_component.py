import logging

from jinja2 import Environment
from .providers import Provider

from .constants import jinja2_component_function


class BaseComponent:
    def __init__(self, 
                 environment: Environment, 
                 cached_data: dict = {}, 
                 persistent_data: dict = {}, 
                 logger = logging.getLogger(__name__),
                 developer_mode: bool = False,
                ) -> None:
        self.providers = {}
        self.environment = environment
        self.logger = logger

        self.cached_data = cached_data
        self.persistent_data = persistent_data

        self.developer_mode = developer_mode
    

    def get_component_data(self, **kwargs):
        """
        Given kwargs from primary template, process them and return some data 
        for the component template.
        """
        return {}


    def render(self, provider: Provider, child_renderer, **component_kwargs) -> str:
        """Uses the Provider and component data to convert the respective component template into a string."""

        # get provider contents (process may vary based on source)
        provider_contents = provider.get_content()

        # convert it into a template, fill in the variables using Jinja2 & return
        component_template = self.environment.from_string(provider_contents)

        return component_template.render({
            **self.get_component_data(**component_kwargs),
            jinja2_component_function: child_renderer
        })
    

    def get_provider_by_key(self, provider_id: str):
        """Fetches the Provider associated with the provided id or raises a KeyError."""

        try:
            return self.providers[provider_id]
        except KeyError:
            raise KeyError(f'Component does not support template provider type: `{provider_id}`!')


    def set_default_provider(self, provider: Provider):
        """Register the default Provider. Replaces if key already exists."""
        self.set_provider('default', provider)


    def set_provider(self, provider_id: str, provider: Provider):
        """Register a new alternate Provider. Replaces if key already exists."""
        self.providers[provider_id] = provider


    def is_provider_set(self, provider_id):
        """Check if a certain provider has been set."""
        return provider_id in self.providers