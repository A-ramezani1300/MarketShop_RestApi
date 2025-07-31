from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        category = Category(name=validated_data['name'], slug=validated_data['slug'])
        category.save()
        return category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'weight', 'quantity', 'price', 'discount_percent', 'inventory']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'product', 'name', 'message', 'created', 'updated']
        read_only_fields = ['id', 'product', 'name', 'created', 'updated']

    def create(self, validated_data):
        name = validated_data.pop('name', None)
        product = validated_data.pop('product', None)
        comment = Comment(message=validated_data['message'], name=name, product=product)
        comment.save()
        return comment

    # def create(self, validated_data):
    #     comment = Comment(message=validated_data['message'])
    #     comment.save()
    #     return comment

    def update(self, instance, validated_data):
        # instance.product = validated_data.get('product', instance.product)
        # instance.name = validated_data.get('name', instance.name)
        instance.message = validated_data.get('message', instance.message)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['name', 'phone', 'title', 'department', 'subject', 'message', 'status', 'created', 'updated']

    def create(self, validated_data):
        ticket = Ticket(name=validated_data['name'], phone=validated_data['phone'], title=validated_data['title'],
                        department=validated_data['department'], subject=validated_data['subject'], message=validated_data['message'])
        ticket.save()
        return ticket


class TicketResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketResponse
        fields = ['ticket', 'user_response', 'message', 'created', 'updated']


    def create(self, validated_data):
        ticket_response = TicketResponse(ticket=validated_data['ticket'], user_response=validated_data['user_response'], message=validated_data['message'])
        ticket_response.save()
        return ticket_response

