from game.models import Category, Game, GameCapture
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.utils import model_meta


class GameCaptureSerializer(serializers.ModelSerializer):
    """Serializer class for GameCapture domain model"""

    class Meta:
        """Meta specs for GameCapture class"""

        model = GameCapture
        fields = ("id", "image")
        extra_kwargs = {"id": {"read_only": False, "required": False}}


class GameSerializer(ModelSerializer):
    captures = GameCaptureSerializer(many=True, required=False, allow_null=True)
    category = serializers.PrimaryKeyRelatedField(
        allow_null=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Game
        fields = "__all__"

    def create(self, validated_data):
        instance = super(GameSerializer, self).create(validated_data)
        images_data = self.context.get("view").request.FILES
        for image_data in images_data.getlist("captures"):
            GameCapture.objects.create(game=instance, image=image_data)
        instance.refresh_from_db()
        return instance

    def update(self, instance, validated_data):
        if self.is_valid(raise_exception=True):
            validated_data = self.data
            info = model_meta.get_field_info(instance)
            try:
                validated_data["category"] = Category.objects.get(
                    id=validated_data["category"]
                )
            except Category.DoesNotExist as err:
                return Response(err, status=status.HTTP_404_NOT_FOUND)
            m2m_fields = []
            for attr, value in validated_data.items():
                if attr in info.relations and info.relations[attr].to_many:
                    m2m_fields.append((attr, value))
                else:
                    setattr(instance, attr, value)

            images_data = self.context.get("view").request.FILES
            instance.captures.clear()
            for image_data in images_data.getlist("captures"):
                GameCapture.objects.create(game=instance, image=image_data)
            instance.save()
            instance.refresh_from_db()
        return instance


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
