from .utils.file import get_file_content

class BaseComponent:
    _type = None
    
    def __init__(self, environment, cached_data, data) -> None:
        self.environment = environment
        self.cached_data = cached_data
        self.providers = {}

        self.data = data

    def render(self, provider_type):
        if (not self.data): return

        template_content = self.get_provider(provider_type)
        template = self.environment.from_string(template_content)
        return template.render(self.data)

    def get_provider(self, provider_type):
        try:
            return self.providers[provider_type]
        except KeyError:
            raise Exception(f'Component does not support template provider type: {provider_type}!')

    def register_provider_type(self, provider_type, path):
        self.providers[provider_type] = get_file_content(path)