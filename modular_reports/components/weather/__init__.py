from ...base_component import BaseComponent

class WeatherComponent(BaseComponent):
    _type = "weather"
    
    def __init__(self, environment, cached_data, **kwargs) -> None:
        data = {
            'location': 'ontario',
            'eleven_am_today': '13 celsius',
            'three_pm_today': '12 celsius',
            'eleven_am_tomorrow': '15 celsius',
            'three_pm_tomorrow': '20 celsius'
        }
        super().__init__(environment, cached_data, data)

        self.register_provider_type('txt', 'modular_reports/components/weather/template.txt')
        self.register_provider_type('mjml', 'modular_reports/components/weather/template.mjml')