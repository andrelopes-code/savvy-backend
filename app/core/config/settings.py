import os
from pathlib import Path

import dotenv
from dynaconf import Dynaconf, Validator

# Get the directory where the current script is located
HERE = Path(__file__).parent
# Load environment variables from the .env file located in the root
dotenv.load_dotenv(HERE.parent.parent.parent / '.env')

# Initialize a Dynaconf settings object
settings = Dynaconf(
    envvar_prefix='SAVVY',
    preload=[os.path.join(HERE, 'default.toml')],
    environments=['development', 'production', 'testing'],
    settings_files=['settings.toml', '.secrets.toml'],
    env_switcher='SAVVY_ENV',
    load_dotenv=False,
)

settings.validators.register(
    Validator('SECRET_KEY', must_exist=True),
)
# Run validators to check if settings are valid
settings.validators.validate()
