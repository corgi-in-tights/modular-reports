import requests, random, os
from ...base_component import BaseComponent

class QuoteComponent(BaseComponent):
    _type = "quote"
    
    def __init__(self, environment, cached_data, **kwargs) -> None:
        self.quote_category = random.choice([
            'funny',
            'inspire'
        ])

        quote = self.get_quote_of_the_day()
        super().__init__(environment, cached_data, quote)

        self.register_provider_type('txt', 'modular_reports/components/quote/template.txt')
        self.register_provider_type('mjml', 'modular_reports/components/quote/template.mjml')

    def get_quote_of_the_day(self):
        url = f'https://quotes.rest/qod?category={self.quote_category}'
        api_token = os.getenv('QUOTE_API_KEY')
        headers = {'content-type': 'application/json', 'X-TheySaidSo-Api-Secret': format(api_token)}

        response = requests.get(url, headers=headers)
        if (response.status_code == 200):
            return response.json()['contents']['quotes'][0]
        else:
            raise Exception(f'Quote API returned response {response.status_code}')