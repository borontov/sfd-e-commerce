from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    """Just an empty serializer for actions that require no input/output data."""
    pass