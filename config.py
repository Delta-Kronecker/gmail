"""
Configuration file for Gmail Creator
"""

# Account creation settings
ACCOUNT_CONFIG = {
    'first_name': 'A',
    'last_name': 'A',
    'password': 'kaaamoooshi',
    'username_pattern': 'kaaamoooshi{index:03d}',
    'total_accounts': 100
}

# Browser settings
BROWSER_CONFIG = {
    'headless': True,
    'timeout': 15,
    'implicit_wait': 5
}

# Delay settings (in seconds)
DELAY_CONFIG = {
    'min_delay': 2.0,
    'max_delay': 5.0,
    'between_accounts_min': 10.0,
    'between_accounts_max': 30.0
}

# GitHub Actions specific
GITHUB_CONFIG = {
    'artifact_retention_days': 7,
    'max_attempts': 3
}
