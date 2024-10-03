import json
from botocore.config import Config
from aws_lambda_powertools.utilities.parameters import SecretsProvider

from .logger import Logger


class AppConfig:
    def __init__(
        self, brand=None, region="eu-west-1", secret_store_name=None, secrets=None
    ):
        self.brand = brand
        self.region = region
        self.secrets = secrets
        self.secret_store_name = secret_store_name
        self.log = Logger.get_logger()
        self.boto_config = Config(region_name=region)
        self.secrets_provider = SecretsProvider(config=self.boto_config)

    def get_secrets(self, max_age=0):
        if not self.secrets:
            self.log.info(f"Fetching secret: {self.secret_store_name}")
            secrets = self.secrets_provider.get(
                name=self.secret_store_name, max_age=max_age
            )
            self.log.info(f"Succesfully got secret: {self.secret_store_name}")
            self.secrets = secrets

        return json.loads(self.secrets)

    def update_secret(self, secret_key_name, value):
        self.log.info(f"Updating secret: {secret_key_name}")
        secrets = self.get_secrets()
        secrets[secret_key_name] = value

        self.secrets_provider.put_secret(self.secret_store_name, json.dumps(secrets))
        self.log.info(f"Succesfully updated secret: {secret_key_name}")
