def currency_symbol_to_code(symbol: str) -> str:
        """
        Convert currency symbol to currency code.
        
        :param symbol: Currency symbol
        :type symbol: str
        :return: Currency code
        :rtype: str
        """
        currency_map = {
            "$": "USD",
            "£": "GBP",
            "€": "EUR",
            "¥": "JPY",
            "₹": "INR",
        }
        return currency_map.get(symbol, symbol)

def combine_key_words(input_ke_words: str) -> str:
    pass