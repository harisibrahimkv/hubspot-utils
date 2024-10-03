from hubspot import HubSpot

from ..pd2lib.logger import Logger
from ..pd2lib.config import AppConfig


class Auth:
    def __init__(self, app_id, brand, secret_store_name, secrets=None):
        self.log = Logger.get_logger()
        self.hubspot = HubSpot()
        self.config = AppConfig(
            brand=brand, secret_store_name=secret_store_name, secrets=secrets
        )
        self.app_id = app_id
        self.secrets = secrets

    def generate_and_save_tokens(self, initial=False):
        if not self.secrets:
            self.secrets = self.config.get_secrets()

        self.log.info(f"Generating tokens")
        tokens = self.hubspot.auth.oauth.tokens_api.create(
            grant_type="refresh_token",
            redirect_uri=self.secrets[f"{self.app_id}_redirect_uri"],
            client_id=self.secrets[f"{self.app_id}_client_id"],
            client_secret=self.secrets[f"{self.app_id}_client_secret"],
            refresh_token=self.secrets[f"{self.app_id}_refresh_token"],
        )
        access_token = tokens.access_token
        refresh_token = tokens.refresh_token

        # TODO: use app_id_access_token instead of `hubspot_access_token`
        # Refer: common_thl/src/pd2lib/config.py: def get_hubspot_api_key
        # self.config.update_secret(f"{self.app_id}_access_token", access_token)
        self.config.update_secret(f"hubspot_access_token", access_token)
        if initial:
            # NOTE: If being used for app installation for the first time
            self.config.update_secret(f"{self.app_id}_refresh_token", refresh_token)

        return access_token
