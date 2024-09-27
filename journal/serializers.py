from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, JournalEntry

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    def update(self, instance, validated_data):
        user = instance
        user.username = validated_data.get('username', user.username)
        user.email = validated_data.get('email', user.email)
        user.set_password(validated_data.get('password', user.password))
        user.save()
        return user
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class JournalEntrySerializer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True)

    class Meta:
        model = JournalEntry
        fields = ["id", "title", "content", "date", "category"]

    def validate_category(self, value):
       
        user = self.context['request'].user
        try:
            Category.objects.get(name=value, user=user)
        except Category.DoesNotExist:
            raise serializers.ValidationError(f"Category '{value}' does not exist for the current user.")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = instance.category.name if instance.category else None
        return representation

    def create(self, validated_data):
        category_name = validated_data.pop('category', None)
        user = self.context['request'].user

        category, _ = Category.objects.get_or_create(name=category_name, user=user)
        validated_data['category'] = category

        journal_entry = super().create(validated_data)
        return journal_entry

    def update(self, instance, validated_data):
        category_name = validated_data.pop('category', None)
        user = self.context['request'].user

        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name, user=user)
            instance.category = category

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.date = validated_data.get('date', instance.date)

        instance.save()
        return instance
    
class JournalEntryFilterSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    filter_by = serializers.ChoiceField(choices=['day', 'week', 'month'], required=False)

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        filter_by = data.get('filter_by')

        if filter_by and (not start_date or not end_date):
            raise serializers.ValidationError("Both start_date and end_date are required when filtering by day, week, or month.")

        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError("Start date cannot be after end date.")

        return data