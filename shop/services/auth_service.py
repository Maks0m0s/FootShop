from django.contrib.auth.models import User

def register(validated_data):
    user = User(
        username=validated_data["username"],
        email=validated_data.get("email", ""),
        first_name=validated_data.get("first_name", ""),
        last_name=validated_data.get("last_name", ""),
    )
    user.set_password(validated_data["password"])
    user.save()

    return user