from rest_framework import serializers
import re

POSTAL_CODE_RULES = {
    "Spain": {
        "regex": r'^\d{5}$',
        "message": "Spanish postal codes must be exactly 5 digits (e.g. 08001)."
    },
    "France": {
        "regex": r'^\d{5}$',
        "message": "French postal codes must be 5 digits (e.g. 75001)."
    },
    "Germany": {
        "regex": r'^\d{5}$',
        "message": "German postal codes must be 5 digits (e.g. 10115)."
    },
    "Italy": {
        "regex": r'^\d{5}$',
        "message": "Italian postal codes must be 5 digits (e.g. 00184)."
    },
    "United Kingdom": {
        "regex": r'^[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}$',
        "message": "UK postal codes must follow formats like SW1A 1AA or M1 1AE."
    },
    "United States": {
        "regex": r'^\d{5}(-\d{4})?$',
        "message": "US ZIP codes must be 5 digits, optionally followed by -4 digits (e.g. 12345 or 12345-6789)."
    },
    "Poland": {
        "regex": r'^\d{2}-\d{3}$',
        "message": "Polish postal codes must follow format 00-000."
    }
}



class CheckoutSerializer(serializers.Serializer):
    country = serializers.CharField(
        max_length=100,
        error_messages={"blank": "Country is required."}
    )
    address = serializers.CharField(
        max_length=255,
        error_messages={"blank": "Address is required."}
    )
    postal_code = serializers.RegexField(
        regex=r'^[A-Za-z0-9\- ]+$',
        max_length=20,
        error_messages={
            'invalid': 'Postal code may contain only letters, digits, spaces, and hyphens.',
            'blank': 'Postal code is required.'
        }
    )

    def validate_country(self, value):
        """Normalize and validate the country name."""
        value = value.strip().title()
        if not re.match(r'^[A-Za-zÀ-ÿ\s\-]+$', value):
            raise serializers.ValidationError("Country must contain only letters and spaces.")
        if len(value) < 3:
            raise serializers.ValidationError("Country name seems too short.")
        return value

    def validate_address(self, value):
        """Ensure the address looks realistic."""
        value = value.strip().title()
        if len(value) < 5:
            raise serializers.ValidationError("Address is too short.")
        if not re.search(r'[A-Za-zÀ-ÿ]', value):
            raise serializers.ValidationError("Address must contain at least one letter.")
        if re.fullmatch(r'\d+', value):
            raise serializers.ValidationError("Address cannot be only numbers.")
        return value

    def validate_postal_code(self, value):
        """Basic postal code validation before cross-checking."""
        value = value.strip().upper()
        if len(value) < 3:
            raise serializers.ValidationError("Postal code seems too short.")
        return value

    def validate(self, data):
        """Cross-field validation — enforce country-specific postal rules."""
        country = data.get("country")
        postal_code = data.get("postal_code")

        if not country or not postal_code:
            raise serializers.ValidationError("Country and postal code are required.")

        rule = POSTAL_CODE_RULES.get(country)
        if rule and not re.match(rule["regex"], postal_code):
            raise serializers.ValidationError({
                "postal_code": rule["message"]
            })

        return data