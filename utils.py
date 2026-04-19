"""
Utility functions for Mercari Auto Price Down App
"""

import re
from urllib.parse import urlparse, parse_qs


def extract_item_id_from_url(url):
    """
    Extract item ID from Mercari URL
    
    Examples:
        https://www.mercari.com/jp/items/m12345678901234/
        → m12345678901234
        
        https://item.mercari.com/jp/m12345678901234/
        → m12345678901234
    """
    # Extract from standard URL format
    match = re.search(r'/items/(m\w+)/?', url)
    if match:
        return match.group(1)
    
    # Extract from item.mercari.com format
    match = re.search(r'/jp/(m\w+)/?', url)
    if match:
        return match.group(1)
    
    # If it looks like an item ID already
    if re.match(r'^m\w+$', url):
        return url
    
    return None


def validate_item_id(item_id):
    """Validate if the string is a valid Mercari item ID"""
    return bool(re.match(r'^m\w{20}$', item_id))


def parse_price(price_str):
    """
    Parse price string to integer
    
    Examples:
        '¥5,000' → 5000
        '5000' → 5000
        '¥5,000円' → 5000
    """
    # Remove currency symbols and commas
    cleaned = re.sub(r'[¥円,\s]', '', price_str)
    
    try:
        return int(cleaned)
    except ValueError:
        return None


def format_price(price):
    """
    Format price for display
    
    Examples:
        5000 → ¥5,000
        100 → ¥100
    """
    return f'¥{price:,}'


def calculate_new_price(current_price, reduce_amount, min_price=100):
    """
    Calculate new price after reduction
    
    Args:
        current_price: Current item price
        reduce_amount: Amount to reduce (default 100)
        min_price: Minimum allowed price (default 100)
    
    Returns:
        New price, ensuring it doesn't go below min_price
    """
    new_price = current_price - reduce_amount
    return max(new_price, min_price)


def get_price_reduction_schedule(current_price, daily_reduction=100, min_price=100):
    """
    Calculate days until item reaches minimum price
    
    Args:
        current_price: Current item price
        daily_reduction: Amount reduced per day
        min_price: Minimum price
    
    Returns:
        Number of days or None if already at minimum
    """
    if current_price <= min_price:
        return 0
    
    difference = current_price - min_price
    days = (difference + daily_reduction - 1) // daily_reduction  # Ceiling division
    return days


def estimate_final_price(current_price, days_to_sell, daily_reduction=100, min_price=100):
    """
    Estimate final price after N days of reductions
    
    Args:
        current_price: Current item price
        days_to_sell: Expected days until item sells
        daily_reduction: Amount reduced per day
        min_price: Minimum price
    
    Returns:
        Estimated final price
    """
    total_reduction = days_to_sell * daily_reduction
    final_price = current_price - total_reduction
    return max(final_price, min_price)


def should_list_on_other_platforms(price, platform_fees=0.1):
    """
    Determine if price is too low to justify platform listing
    
    Args:
        price: Item price
        platform_fees: Platform fee percentage (default 10%)
    
    Returns:
        True if price is profitable enough
    """
    fee = price * platform_fees
    profit_threshold = 100  # Minimum acceptable profit
    return (price - fee) > profit_threshold


def batch_parse_items(item_data_list):
    """
    Parse a batch of items for price reduction
    
    Args:
        item_data_list: List of dicts with 'id' and 'price' keys
    
    Returns:
        List of processed items with validation
    """
    processed = []
    
    for item in item_data_list:
        item_id = item.get('id') or extract_item_id_from_url(item.get('url', ''))
        price = item.get('price')
        
        if isinstance(price, str):
            price = parse_price(price)
        
        if item_id and validate_item_id(item_id) and price and price > 0:
            processed.append({
                'id': item_id,
                'price': price,
                'formatted_price': format_price(price)
            })
    
    return processed


if __name__ == '__main__':
    # Example usage
    print('Utility Functions Examples:')
    print()
    
    # Extract item ID
    url = 'https://www.mercari.com/jp/items/m123456789012345678/'
    item_id = extract_item_id_from_url(url)
    print(f'Extract ID from URL: {url}')
    print(f'  Result: {item_id}')
    print()
    
    # Parse price
    price_str = '¥5,000'
    price = parse_price(price_str)
    print(f'Parse price: {price_str}')
    print(f'  Result: {price}')
    print()
    
    # Calculate new price
    current = 5000
    new = calculate_new_price(current, 100)
    print(f'Calculate new price: {format_price(current)} - ¥100')
    print(f'  Result: {format_price(new)}')
    print()
    
    # Get reduction schedule
    days = get_price_reduction_schedule(5000, 100, 100)
    print(f'Days to reach minimum price (¥5000 → ¥100):')
    print(f'  Result: {days} days')
    print()
    
    # Estimate final price
    final = estimate_final_price(5000, 14, 100)
    print(f'Estimate price after 14 days:')
    print(f'  Result: {format_price(final)}')
