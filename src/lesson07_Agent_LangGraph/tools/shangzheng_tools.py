from bs4 import BeautifulSoup
import requests

# New tool for fetching 上证指数 data
def fetch_shangzheng_data(query: str) -> str:
    """Fetches the latest 上证指数 data from the specified URL."""
    url = "https://gushitong.baidu.com/index/ab-000001"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        # Update with the appropriate class or tag based on the webpage structure
        index_data = soup.find("div", class_="index-value").text.strip()  
        return f"上证指数: {index_data}"
    except Exception as e:
        return f"Failed to fetch 上证指数 data: {str(e)}"

# Add ShangZhengIndex tool
class ShangZhengTool:
    def __init__(self):
        self.name = "ShangZhengIndex"
        self.description = "Fetch the latest 上证指数 data."
    
    def invoke(self, query: str) -> str:
        return fetch_shangzheng_data(query)