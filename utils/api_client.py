import requests
from urllib.parse import quote

class SwissTourismAPI:
    def __init__(self):
        self.base_url = "https://opendata.myswitzerland.io/v1"
        self.headers = {
            "x-api-key": "jp8qBDqD7HaPZz1XsSmD7W03Zm1RoWj9I9Js5Nai"
        }
    
    def get_destination_info(self, destination_name, language="en", limit=5):
        """Get detailed information about a destination"""
        url = f"{self.base_url}/destinations"
        params = {
            "lang": language,
            "limit": limit,
            "query": quote(destination_name)
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data and 'data' in data and len(data['data']) > 0:
                # Extract relevant information from the first matching destination
                destination = data['data'][0]
                return {
                    'name': destination.get('name', ''),
                    'abstract': destination.get('abstract', ''),
                    'url': destination.get('url', ''),
                    'photo': destination.get('photo', ''),
                    'geo': destination.get('geo', {}),
                    'classifications': self._extract_classifications(destination.get('classification', [])),
                    'links': destination.get('links', {})
                }
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching destination info: {e}")
            return None
    
    def _extract_classifications(self, classifications):
        """Extract and organize classification information"""
        result = {}
        for classification in classifications:
            name = classification.get('name', '')
            values = classification.get('values', [])
            if name and values:
                result[name] = [value.get('title', '') for value in values]
        return result

# Create a global instance
api_client = SwissTourismAPI() 