import os
from pathlib import Path

import dotenv
from dynaconf import Dynaconf

# Get the directory where the current script is located
HERE = Path(__file__).parent
# Load environment variables from the .env file located in the root
dotenv.load_dotenv(HERE.parent.parent.parent / '.env')

# Initialize a Dynaconf settings object
settings = Dynaconf(
    # Prefix for environment variables
    envvar_prefix='SAVVY',
    # Preload default settings from 'default.toml'
    preload=[os.path.join(HERE, 'default.toml')],
    # Define different environments
    environments=['development', 'production', 'testing'],
    # Specify settings files to load
    settings_files=['settings.toml', '.secrets.toml'],
    # Environment variable to switch between environments
    env_switcher='SAVVY_ENV',
    # Disable loading environment variables from a .env file
    load_dotenv=False,
)
