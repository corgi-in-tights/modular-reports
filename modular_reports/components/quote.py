import requests, os, random

from modular_reports.base_component import BaseComponent
from modular_reports.providers import FileProvider
from modular_reports.utils import get_component_template_path

class QuoteComponent(BaseComponent):
    component_id = 'base:quote'
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_default_provider(FileProvider(get_component_template_path('quote/template.txt')))
        self.set_provider('mjml', FileProvider(get_component_template_path('quote/template.mjml')))

    def get_component_data(self, hello, **kwargs):
        if (self.developer_mode): 
            return {
                'quote': 'Developer mode has been turned on.',
                'author': 'modular-reports'
            }
        
        # declare template variables 
        quote_category = random.choice([
            'funny',
            'inspire'
        ])

        url = f'https://quotes.rest/qod?category={quote_category}'
        api_key = os.getenv('QUOTE_API_KEY')
        headers = {'content-type': 'application/json', 'X-TheySaidSo-Api-Secret': format(api_key)}

        response = requests.get(url, headers=headers)
        if (response.status_code == 200):
            return response.json()['contents']['quotes'][0]
        
        raise Exception(f'Quote API returned response {response.status_code}')