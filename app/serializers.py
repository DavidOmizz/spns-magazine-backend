from rest_framework import serializers
from .models import Article, Edition, Contributor, User, PDFRequest, EditionRequest



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type',]
        extra_kwargs = {
            'email': {'required': True},
            'user_type': {'required': True},
        }

    def create(self, validated_data):
        # Use the create_user method to ensure the password is hashed
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data.get('user_type', 'free'),
        )

class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')  # Gets the username from the User model
    bio = serializers.CharField()
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'bio', 'full_name', 'profile_picture']

## Working
# class EditionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Edition
#         fields = ['id', 'name', 'description', 'release_date']

class EditionSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Edition
        fields = ['id', 'name', 'description', 'release_date', 'download_url', 'articles', 'coverimage', 'pdf_file']

    def get_articles(self, obj):
        articles = obj.articles.all()
        return ArticleSerializer(articles, many=True, context=self.context).data

    def get_download_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/editions/{obj.id}/download_articles/')



# Working
# class ArticleSerializer(serializers.ModelSerializer):
#     contributor = ContributorSerializer(read_only=True)
#     edition = serializers.PrimaryKeyRelatedField(queryset=Edition.objects.all())

#     class Meta:
#         model = Article
#         fields = ['id', 'title', 'content', 'image', 'contributor', 'edition', 'publication_date']

# class ArticleSerializer(serializers.ModelSerializer):
#     content_preview = serializers.SerializerMethodField()
#     download_link = serializers.SerializerMethodField()

#     class Meta:
#         model = Article
#         fields = ['id', 'title', 'content_preview', 'download_link', 'publication_date', 'contributor', 'edition']

#     def get_content_preview(self, obj):
#         # Return the first 100 characters of the content
#         return obj.content[:100] + "..."

#     def get_download_link(self, obj):
#         # Assume you have an endpoint for generating article PDFs
#         request = self.context.get('request')
#         return request.build_absolute_uri(f'/api/articles/{obj.id}/download/')

# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = [
#             'id', 'title', 'content', 'image', 'contributor', 
#             'edition', 'publication_date', 'pdf_file'
#         ]
#         read_only_fields = ['contributor']

class ArticleSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()
    # Include the Contributor details in the Article serializer
    contributor = ContributorSerializer()
    industry_display = serializers.CharField(source='get_industry_display', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'image', 'contributor', 
            'edition', 'publication_date', 'pdf_file', 'pdf_url', 'industry', 'industry_display'
        ]
        read_only_fields = ['contributor']

    # def get_pdf_url(self, obj):
    #     request = self.context.get('request')
    #     if obj.pdf_file:
    #         return request.build_absolute_uri(obj.pdf_file.url)
    #     return None

    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.pdf_file:
            file_url = obj.pdf_file.url
            # Ensure the URL ends with .pdf
            if not file_url.endswith('.pdf'):
                file_url += '.pdf'
            return request.build_absolute_uri(file_url)
        return None

class PDFRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFRequest
        fields = ['name', 'email', 'phone_number', 'company', 'job_title']

class EditionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditionRequest
        fields = ['name', 'email', 'phone_number', 'company', 'job_title']

