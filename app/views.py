from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Article, Edition, Contributor, User, PDFRequest, EditionRequest
from .serializers import ArticleSerializer, EditionSerializer, ContributorSerializer, RegisterSerializer, PDFRequestSerializer, EditionRequestSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reportlab.pdfgen import canvas
from io import BytesIO
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter


from django.contrib.auth import authenticate, login


# class LoginView(APIView):
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         if not username or not password:
#             return Response(
#                 {"error": "Username and password are required."}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)  # Logs the user into the session (if using session-based authentication)
#             return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
#         else:
#             return Response(
#                 {"error": "Invalid username or password."}, 
#                 status=status.HTTP_401_UNAUTHORIZED
#             )


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Username and password are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "refresh": str(refresh),
                "access": access_token
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid username or password."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "user_type": user.user_type,
            },
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

# class EditionViewSet(viewsets.ModelViewSet):
#     queryset = Edition.objects.all()
#     serializer_class = EditionSerializer

# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         # Automatically associate the logged-in user as the contributor
#         serializer.save(contributor=self.request.user.contributor)



## Working
# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         # Automatically associate the logged-in user as the contributor
#         serializer.save(contributor=self.request.user.contributor)

#     @action(detail=True, methods=['get'])
#     def download(self, request, pk=None):
#         # Retrieve the article object
#         article = self.get_object()

#         # Generate PDF content
#         buffer = BytesIO()
#         pdf = canvas.Canvas(buffer)
#         pdf.drawString(100, 800, f"Title: {article.title}")
#         pdf.drawString(100, 780, f"Contributor: {article.contributor}")
#         pdf.drawString(100, 760, f"Publication Date: {article.publication_date}")
#         pdf.drawString(100, 740, "Content:")
#         pdf.drawString(100, 720, article.content[:1000])  # Truncate long content for demo purposes

#         pdf.save()
#         buffer.seek(0)

#         # Return the PDF file as a response
#         response = HttpResponse(buffer, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="article_{article.id}.pdf"'
#         return response

# from reportlab.lib.pagesizes import letter
# from reportlab.lib import utils

# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         serializer.save(contributor=self.request.user.contributor)

#     @action(detail=True, methods=['get'])
#     def download(self, request, pk=None):
#         article = self.get_object()

#         # Prepare PDF
#         buffer = BytesIO()
#         pdf = canvas.Canvas(buffer, pagesize=letter)
#         width, height = letter  # Page dimensions
#         x_margin = 50  # Left margin
#         y_start = height - 50  # Start from top with some margin

#         # Write Title and Metadata
#         pdf.setFont("Helvetica-Bold", 16)
#         pdf.drawString(x_margin, y_start, f"Title: {article.title}")
#         y_start -= 20
#         pdf.setFont("Helvetica", 12)
#         pdf.drawString(x_margin, y_start, f"Contributor: {article.contributor}")
#         y_start -= 20
#         pdf.drawString(x_margin, y_start, f"Publication Date: {article.publication_date}")
#         y_start -= 40  # Space before content

#         # Wrap Content Text
#         content = article.content
#         text_object = pdf.beginText(x_margin, y_start)
#         text_object.setFont("Helvetica", 12)
#         text_object.setTextOrigin(x_margin, y_start)

#         max_width = width - (2 * x_margin)  # Text wrapping width
#         lines = self._wrap_text(content, max_width, pdf)

#         for line in lines:
#             if y_start < 50:  # Check if a new page is needed
#                 pdf.showPage()
#                 y_start = height - 50
#                 text_object = pdf.beginText(x_margin, y_start)
#                 text_object.setFont("Helvetica", 12)

#             text_object.textLine(line)
#             y_start -= 15

#         pdf.drawText(text_object)
#         pdf.save()
#         buffer.seek(0)

#         # Return PDF as Response
#         response = HttpResponse(buffer, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="article_{article.id}.pdf"'
#         return response

#     def _wrap_text(self, text, max_width, pdf):
#         """
#         Helper method to wrap text to fit within a specific width.
#         """
#         from reportlab.pdfbase.pdfmetrics import stringWidth
#         words = text.split()
#         lines = []
#         current_line = []

#         for word in words:
#             current_line.append(word)
#             line_width = stringWidth(' '.join(current_line), pdf._fontname, pdf._fontsize)
#             if line_width > max_width:
#                 # Line too long, wrap
#                 current_line.pop()  # Remove last word
#                 lines.append(' '.join(current_line))
#                 current_line = [word]  # Start a new line with the word

#         if current_line:
#             lines.append(' '.join(current_line))

#         return lines


# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         # Automatically associate the logged-in user as the contributor
#         serializer.save(contributor=self.request.user.contributor)

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from cloudinary.utils import cloudinary_url
from django.db.models import Q

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    # search_fields = ['title', 'content', 'contributor__name']
    search_fields = [
        'title', 
        'content', 
        'contributor__name',  # Search by contributor name
        'industry',           # Search by industry
        'edition__name'       # Search by edition name
    ]

    def perform_create(self, serializer):
        serializer.save(contributor=self.request.user.contributor)

    @action(detail=True, methods=['post'])
    def request_pdf(self, request, pk=None):
        article = self.get_object()  # Get the article instance
        serializer = PDFRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the PDF request form data
            pdf_request = serializer.save(article=article)
            
            # Send PDF via email
            pdf_file_url = article.pdf_file.url
            # pdf_url, options = cloudinary_url(article.pdf_file.name, resource_type="raw")

            # Ensure the correct URL for the PDF with the 'raw' resource type
            # pdf_file_url, options = cloudinary_url(article.pdf_file.name, access_mode="public")

            # Get the domain dynamically
            current_site = get_current_site(request)  # 'request' is the HttpRequest object
            domain = current_site.domain  # Get the domain name (example: example.com)

            # Build the full PDF URL with http/https scheme based on the request
            scheme = request.scheme  # 'http' or 'https' based on the request
            full_pdf_url = f"{scheme}://{domain}{pdf_file_url}"
            subject = f"Your requested PDF: {article.title}"
             # Prepare the email subject and message
            subject = f"Your requested PDF: {article.title}"
            # message = f"""
            # <html>
            #     <body>
            #         <p>Hello {pdf_request.name},</p>
            #         <p>Thank you for requesting the PDF for the article <strong>'{article.title}'</strong>.</p>
            #         <p>You can download it using the link below:</p>
            #         <p><a href="{full_pdf_url}">Download PDF</a></p>
            #         <p>Best regards,<br>Your Article Team</p>
            #     </body>
            # </html>
            # """
            
            message = f"Hello {pdf_request.name},\n\nThank you for requesting the PDF for the article '{article.title}'. You can download it using the link below:\n\n{pdf_file_url}\n\nBest regards,\nBPPR Team"
            recipient_list = [pdf_request.email]
            # recipient_list = [pdf_request.email]
            
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
                return Response({'message': 'PDF request submitted successfully. You will receive the PDF via email.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
        Custom queryset to handle year-based filtering.
        """
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            # Check if the query is numeric and of length 4 (likely a year)
            if search_query.isdigit() and len(search_query) == 4:
                queryset = queryset.filter(
                    Q(publication_date__year=search_query) |
                    Q(title__icontains=search_query) |
                    Q(content__icontains=search_query) |
                    Q(contributor__full_name__icontains=search_query)|
                    Q(industry__icontains=search_query) |
                    Q(edition__name__icontains=search_query)
                )
            else:
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(content__icontains=search_query) |
                    Q(contributor__full_name__icontains=search_query) |
                    Q(industry__icontains=search_query) |
                    Q(edition__name__icontains=search_query)
                )
        return queryset

    
## Working
# class EditionViewSet(viewsets.ModelViewSet):
#     queryset = Edition.objects.all()
#     serializer_class = EditionSerializer

#     @action(detail=True, methods=['get'])
#     def download(self, request, pk=None):
#         edition = self.get_object()
#         articles = edition.articles.all()
        
#         # Generate PDF content
#         buffer = BytesIO()
#         pdf = canvas.Canvas(buffer)
#         y = 800
#         pdf.drawString(100, y, f"Edition: {edition.id}")
#         y -= 20
        
#         for article in articles:
#             pdf.drawString(100, y, f"Title: {article.title}")
#             y -= 20
#             pdf.drawString(100, y, f"Contributor: {article.contributor}")
#             y -= 20
#             pdf.drawString(100, y, f"Publication Date: {article.publication_date}")
#             y -= 20
#             pdf.drawString(100, y, f"Content Preview: {article.content[:100]}")
#             y -= 40  # Leave space between articles

#             if y < 100:  # Start a new page if there's no space
#                 pdf.showPage()
#                 y = 800

#         pdf.save()
#         buffer.seek(0)

#         # Return the PDF file as a response
#         response = HttpResponse(buffer, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="edition_{edition.id}.pdf"'
#         return response



import os
from zipfile import ZipFile
# class EditionViewSet(viewsets.ModelViewSet):
#     queryset = Edition.objects.all()
#     serializer_class = EditionSerializer

#     @action(detail=True, methods=['get'])
#     def download_articles(self, request, pk=None):
#         # Get the edition and its related articles
#         edition = self.get_object()
#         articles = edition.articles.all()  # Related name for the foreign key

#         # Create a zip file in memory
#         buffer = BytesIO()
#         with ZipFile(buffer, 'w') as zip_file:
#             for article in articles:
#                 if article.pdf_file:
#                     # Add each article's PDF file to the zip
#                     file_path = article.pdf_file.path
#                     file_name = os.path.basename(file_path)
#                     zip_file.write(file_path, f"{edition.name}/{file_name}")

#         buffer.seek(0)

#         # Return the zip file as a downloadable response
#         response = HttpResponse(buffer, content_type='application/zip')
#         response['Content-Disposition'] = f'attachment; filename="edition_{edition.id}_articles.zip"'
#         return response

#     @action(detail=True, methods=['get'])
#     def articles(self, request, pk=None):
#         """
#         Retrieve all articles related to a specific edition.
#         """
#         edition = self.get_object()
#         articles = edition.articles.all()  # Assuming the related name is `articles`
#         # serializer = ArticleSerializer(articles, many=True)
#         serializer = ArticleSerializer(articles, many=True, context={'request': request})
#         return Response(serializer.data)
#         # return Response(serializer.data)

#     @action(detail=True, methods=['post'])
#     def request_edition(self, request, pk=None):
#         edition = self.get_object()  # Get the article instance
#         serializer = EditionRequestSerializer(data=request.data)
        
#         if serializer.is_valid():
#             # Save the PDF request form data
#             edition_request = serializer.save(edition=edition)
            
#             # Send PDF via email
#             edition_file_url = edition.pdf_file.url
#             # Get the domain dynamically
#             current_site = get_current_site(request)  # 'request' is the HttpRequest object
#             domain = current_site.domain  # Get the domain name (example: example.com)

#             # Build the full PDF URL with http/https scheme based on the request
#             scheme = request.scheme  # 'http' or 'https' based on the request
#             full_pdf_url = f"{scheme}://{domain}{edition_file_url}"
#             subject = f"Your requested PDF: {edition.name}"
#              # Prepare the email subject and message
#             subject = f"Your requested PDF: {edition.name}"
#             # message = f"""
#             # <html>
#             #     <body>
#             #         <p>Hello {pdf_request.name},</p>
#             #         <p>Thank you for requesting the PDF for the article <strong>'{article.title}'</strong>.</p>
#             #         <p>You can download it using the link below:</p>
#             #         <p><a href="{full_pdf_url}">Download PDF</a></p>
#             #         <p>Best regards,<br>Your Article Team</p>
#             #     </body>
#             # </html>
#             # """
            
#             message = f"Hello {edition_request.name},\n\nThank you for requesting the PDF for the Edition '{edition.name}'. You can download it using the link below:\n\n{full_pdf_url}\n\nBest regards,\nBPPR Team"
#             recipient_list = [edition_request.email]
#             # recipient_list = [pdf_request.email]
            
#             try:
#                 send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
#                 return Response({'message': 'Edition request submitted successfully. You will receive the PDF via email.'}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditionViewSet(viewsets.ModelViewSet):
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer
    search_fields = [
        'name', 
        'description', 
        'articles__title',  # Search articles within editions
        'articles__contributor__name',  # Search by contributor in articles
        'articles__industry',  # Search by industry in articles
    ]

    @action(detail=True, methods=['get'])
    def articles(self, request, pk=None):
        """
        Retrieve all articles related to a specific edition.
        """
        edition = self.get_object()
        articles = edition.articles.all()  # Assuming the related name is `articles`
        # serializer = ArticleSerializer(articles, many=True)
        serializer = ArticleSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)
        # return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='request_pdf')
    def request_pdf(self, request, pk=None):
        edition = self.get_object()  # Get the edition instance by ID
        serializer = EditionRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the PDF request data
            edition_request = serializer.save(edition=edition)
            
            # Send the PDF via email
            edition_file_url = edition.pdf_file.url  # Assuming the edition has a `pdf_file` field
            current_site = get_current_site(request)
            domain = current_site.domain
            scheme = request.scheme
            full_pdf_url = f"{scheme}://{domain}{edition_file_url}"

            subject = f"Your requested PDF: {edition.name}"
            message = f"Hello {edition_request.name},\n\nThank you for requesting the PDF for the Edition '{edition.name}'. You can download it using the link below:\n\n{edition_file_url}\n\nBest regards,\nYour Team"
            recipient_list = [edition_request.email]

            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
                return Response({'message': 'Edition request submitted successfully. You will receive the PDF via email.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)