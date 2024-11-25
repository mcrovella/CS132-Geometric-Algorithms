"""YAML configuration printer for Quarto.

This script prints the merged configuration settings for a Quarto project. It
loads the main _quarto.yml file and then checks if a profile is active. If a
profile is active, it loads the corresponding _quarto-{profile}.yml file and
merges the two configurations. The merged configuration is then printed as a
nicely formatted YAML string and also saved to a file named config_log.yml.

Note that this _might not_ be how Quarto actually merges the configurations, but
it should give a good idea of how the configurations are merged.

Example commands:

# Run the script without a profile or with the default profile
$ quarto run print_quarto_config.py

# Run the script with a specific profile set as environment variable
$ QUARTO_PROFILE=production quarto run print_quarto_config.py

# Run the script with a specific profile set as command line option
$ quarto run print_quarto_config.py --profile slides
"""
import os
import yaml

PRINT_ALL_ENV_VARS = False

# Load the main _quarto.yml file
with open('_quarto.yml', 'r') as file:
    main_config = yaml.safe_load(file)

# Iterate through all environment variables and print them
if PRINT_ALL_ENV_VARS:
    print('\nAll environment variables:')
    for key, value in os.environ.items():
        print(f"{key}: {value}")

# Filter and print environment variables that start with 'QUARTO_'
print('\nQUARTO environment variables:')
quarto_vars = {key: value for key, value in os.environ.items() if key.startswith('QUARTO_')}
for key, value in quarto_vars.items():
    print(f"{key}: {value}")

# Filter and print environment variables that start with 'DENO_'
print('\nDENO environment variables:')
quarto_vars = {key: value for key, value in os.environ.items() if key.startswith('DENO_')}
for key, value in quarto_vars.items():
    print(f"{key}: {value}")

print('\n')

# Check if a profile is active and load the corresponding YAML file
profile = os.getenv('QUARTO_PROFILE')
if profile:
    print(f'Environemnt variable QUARTO_PROFILE = {profile}')
    profile_config_file = f'_quarto-{profile}.yml'
    if os.path.exists(profile_config_file):
        with open(profile_config_file, 'r') as file:
            profile_config = yaml.safe_load(file)
        # Merge profile config with main config (profile overrides main)
        merged_config = {**main_config, **profile_config}
    else:
        print(f'Profile file {profile_config_file} not found')
        merged_config = main_config
else:
    print('No QUARTO_PROFILE set')
    merged_config = main_config

# Convert the merged configuration to a YAML string
print('\nMerged configuration:\n')
yaml_str = yaml.dump(merged_config, default_flow_style=False)

# Print the nicely formatted YAML string
print(yaml_str)

# Print out all the settings
# print(merged_config)

with open('config_log.yml', 'w') as file:
    yaml.dump(merged_config, file)

print('Configuration saved to config_log.yml')

print('\nReminder: This script might not accurately reflect how Quarto merges configurations.')
print('It is intended as a simple tool to help understand the configuration settings.')
print('For the most accurate information, consult the Quarto documentation.')
