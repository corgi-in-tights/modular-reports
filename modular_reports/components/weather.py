import requests, os

from modular_reports.base_component import BaseComponent
from modular_reports.providers import FileProvider
from modular_reports.utils import get_component_template_path

class WeatherComponent(BaseComponent):
    component_id = 'base:weather'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_default_provider(FileProvider(get_component_template_path('weather/template.txt')))
        self.set_provider('mjml', FileProvider(get_component_template_path('weather/template.mjml')))

    def get_component_data(self, lat, lon, **kwargs):
        if (self.developer_mode):
            return {
                'location': 'ontario',
                'eleven_am_today': '13 celsius',
                'three_pm_today': '12 celsius',
                'eleven_am_tomorrow': '15 celsius',
                'three_pm_tomorrow': '20 celsius'
            }
    
        api_key = os.getenv('WEATHER_API_KEY')
        print (api_key)
        url = f'https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=1&appid={api_key}'

        response = requests.get(url)
        print (response)

        if (response.status_code == 200):
            print (response.json())
            return response.json()
        
        raise Exception(f'Weather API returned response {response.status_code}')