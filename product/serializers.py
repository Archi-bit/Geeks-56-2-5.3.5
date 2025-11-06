from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название категории не может быть пустым.")
        if Category.objects.filter(name__iexact=value.strip()).exists():
            raise serializers.ValidationError("Такая категория уже существует.")
        return value.strip()


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    rating = serializers.SerializerMethodField(read_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'rating', 'reviews']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной.")
        return value

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Название товара должно быть длиной минимум 3 символа.")
        return value.strip()

    def get_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        return round(avg, 1) if avg else None

    def get_reviews(self, obj):
        from .serializers import ReviewSerializer
        reviews = obj.reviews.all()
        return ReviewSerializer(reviews, many=True).data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']

    def validate_stars(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Рейтинг (stars) должен быть от 1 до 5.")
        return value

    def validate_text(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Текст отзыва должен быть минимум 10 символов.")
        return value.strip()

    def validate(self, data):
        if Review.objects.filter(product=data['product'], text__iexact=data['text']).exists():
            raise serializers.ValidationError("Похожий отзыв на этот товар уже существует.")
        return data