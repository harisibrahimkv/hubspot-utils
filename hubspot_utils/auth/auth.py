from hubspot import HubSpot

from ..pd2lib.logger import Logger
from ..pd2lib.config import AppConfig


class Auth:
    def __init__(self, app_id, brand, secret_store_name):
        self.log = Logger.get_logger()
        self.hubspot = HubSpot()
        self.config = AppConfig(brand=brand, secret_store_name=secret_store_name)
        self.app_id = app_id

    def generate_and_save_tokens(self, initial=False):
        secrets = self.config.get_secrets()

        self.log.info(f"Generating tokens")
        tokens = self.hubspot.auth.oauth.tokens_api.create(
            grant_type="refresh_token",
            redirect_uri=secrets[f"{self.app_id}_redirect_uri"],
            client_id=secrets[f"{self.app_id}_client_id"],
            client_secret=secrets[f"{self.app_id}_client_secret"],
            refresh_token=secrets[f"{self.app_id}_refresh_token"]
        )
        access_token = tokens.access_token
        refresh_token = tokens.refresh_token

        # TODO: use app_id_access_token instead of `hubspot_access_token`
        # self.config.update_secret(f"{self.app_id}_access_token", access_token)
        self.config.update_secret(f"hubspot_access_token", access_token)
        if initial:
            self.config.update_secret(f"{self.app_id}_refresh_token", refresh_token)

        return access_token