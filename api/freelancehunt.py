import requests
import re
from transliterate import translit
from config import settings
from utils.logger import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


class FreelancehuntAPI:
    def __init__(self):
        self.token = settings.FH_TOKEN
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.base_url = "https://api.freelancehunt.com/v2"

    @retry(
        retry=retry_if_exception_type(requests.RequestException),
        wait=wait_exponential(multiplier=1, min=4, max=30),
        stop=stop_after_attempt(5),
    )
    def get_new_projects(self, limit: int = 20):
        url = f"{self.base_url}/projects?sort_field=created&limit={limit}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json().get("data", [])
            logger.error(f"FH API Error: {response.status_code} - {response.text}")
            return []
        except requests.RequestException as e:
            logger.error(f"FH API Connection Error: {e}")
            raise

    def get_employer_info(self, employer_id: int):
        url = f"{self.base_url}/employers/{employer_id}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json().get("data", {}).get("attributes", {})
        except Exception as e:
            logger.error(f"Error fetching employer {employer_id}: {e}")
        return {}

    @staticmethod
    def slugify(text: str) -> str:
        text = translit(text, "ru", reversed=True)
        text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower())
        text = re.sub(r"-+", "-", text).strip("-")
        return text

    def get_project_link(self, project_id: int, title: str) -> str:
        slug = self.slugify(title)
        return f"https://freelancehunt.com/project/{slug}/{project_id}.html"
