from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file=serializers.FileField()

    def validate_file(self, value):
        if not (value.name.endswith('.csv') or value.name.endswith('.xlsx')):
            raise serializers.ValidationError("Only CSV and XLSX files are allowed.")
        return value