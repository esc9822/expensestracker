# ============================================================
# EXPENSE TRACKER CONFIGURATION
# Author: Edward Colon (ESC)
# Copyright (c) 2026
# ============================================================

# MODE: 'PERSONAL' (single user, no login) or 'CORPORATE' (multi-user with login)
MODE = 'PERSONAL'

# Default country and currency
DEFAULT_COUNTRY = 'Philippines'
DEFAULT_CURRENCY = 'PHP'

# ============================================================
# CURRENCY CONVERSION
# ============================================================

# Fallback rates (used if API fails)
FALLBACK_CONVERSION_RATES = {
    'PHP': 1.0,
    'USD': 0.018,
    'GBP': 0.014,
    'EUR': 0.017,
    'JPY': 2.65,
    'AUD': 0.028,
    'CAD': 0.025,
    'SGD': 0.024,
    'HKD': 0.14,
    'KRW': 24.0,
}

CONVERSION_RATES = FALLBACK_CONVERSION_RATES.copy()
CURRENCY_API_URL = 'https://api.exchangerate-api.com/v4/latest/PHP'

# Country to Currency mapping
COUNTRIES = {
    'Philippines': {'currency': 'PHP', 'symbol': '₱', 'flag': '🇵🇭'},
    'United States': {'currency': 'USD', 'symbol': '$', 'flag': '🇺🇸'},
    'United Kingdom': {'currency': 'GBP', 'symbol': '£', 'flag': '🇬🇧'},
    'European Union': {'currency': 'EUR', 'symbol': '€', 'flag': '🇪🇺'},
    'Japan': {'currency': 'JPY', 'symbol': '¥', 'flag': '🇯🇵'},
    'Australia': {'currency': 'AUD', 'symbol': 'A$', 'flag': '🇦🇺'},
    'Canada': {'currency': 'CAD', 'symbol': 'C$', 'flag': '🇨🇦'},
    'Singapore': {'currency': 'SGD', 'symbol': 'S$', 'flag': '🇸🇬'},
    'Hong Kong': {'currency': 'HKD', 'symbol': 'HK$', 'flag': '🇭🇰'},
    'South Korea': {'currency': 'KRW', 'symbol': '₩', 'flag': '🇰🇷'},
}

def get_country_info(country_name):
    """Get currency info for a country"""
    return COUNTRIES.get(country_name, COUNTRIES[DEFAULT_COUNTRY])

def get_currency_symbol(country_name=None):
    """Get the currency symbol for the selected country"""
    if country_name and country_name in COUNTRIES:
        return COUNTRIES[country_name]['symbol']
    return COUNTRIES[DEFAULT_COUNTRY]['symbol']

def convert_to_base(amount, from_currency):
    """Convert from any currency to base currency (PHP)"""
    if from_currency == 'PHP':
        return amount
    rate = CONVERSION_RATES.get(from_currency, 1.0)
    # If 1 PHP = X currency, then 1 currency = 1/X PHP
    return amount / rate

def convert_from_base(amount, to_currency):
    """Convert from base currency (PHP) to any currency"""
    if to_currency == 'PHP':
        return amount
    rate = CONVERSION_RATES.get(to_currency, 1.0)
    return amount * rate

def get_conversion_rate(from_currency, to_currency):
    """Get the conversion rate between two currencies"""
    if from_currency == to_currency:
        return 1.0
    # Convert to base, then to target
    base_amount = convert_to_base(1.0, from_currency)
    return convert_from_base(base_amount, to_currency)

def fetch_live_rates():
    """Fetch live currency rates from API with 24-hour caching"""
    global CONVERSION_RATES
    
    import urllib.request
    import json
    from datetime import datetime
    import database as db
    
    cached_rates, last_update = db.get_currency_rates()
    
    if cached_rates and last_update:
        try:
            update_time = datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
            hours_since_update = (datetime.now() - update_time).total_seconds() / 3600
            
            if hours_since_update < 24:
                CONVERSION_RATES.update(cached_rates)
                return True, f"Using cached rates (updated {int(hours_since_update)} hours ago)"
        except:
            pass
    
    try:
        with urllib.request.urlopen(CURRENCY_API_URL, timeout=5) as response:
            data = json.loads(response.read().decode())
            
        if 'rates' in data:
            new_rates = {
                'PHP': 1.0,
                'USD': data['rates'].get('USD', FALLBACK_CONVERSION_RATES['USD']),
                'GBP': data['rates'].get('GBP', FALLBACK_CONVERSION_RATES['GBP']),
                'EUR': data['rates'].get('EUR', FALLBACK_CONVERSION_RATES['EUR']),
                'JPY': data['rates'].get('JPY', FALLBACK_CONVERSION_RATES['JPY']),
                'AUD': data['rates'].get('AUD', FALLBACK_CONVERSION_RATES['AUD']),
                'CAD': data['rates'].get('CAD', FALLBACK_CONVERSION_RATES['CAD']),
                'SGD': data['rates'].get('SGD', FALLBACK_CONVERSION_RATES['SGD']),
                'HKD': data['rates'].get('HKD', FALLBACK_CONVERSION_RATES['HKD']),
                'KRW': data['rates'].get('KRW', FALLBACK_CONVERSION_RATES['KRW']),
            }
            
            db.update_currency_rates(new_rates)
            CONVERSION_RATES = new_rates
            return True, "Live rates fetched successfully!"
    except Exception as e:
        CONVERSION_RATES = FALLBACK_CONVERSION_RATES.copy()
        return False, f"API failed, using fallback rates"
