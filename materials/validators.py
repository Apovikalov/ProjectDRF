from rest_framework import serializers


def validate_no_links(value):
    if "https://" in value and "https://youtube.com" not in value:
        raise serializers.ValidationError("В материалах не должно быть ссылок на ресурсы, кроме YouTube.")
