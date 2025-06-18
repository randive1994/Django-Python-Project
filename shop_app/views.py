from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError, NotFound, APIException
from django.db import transaction,IntegrityError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from .models import Book, Product, User
from .serializers import BookSerializer, ProductSerializer, UserSerializer, LogoutResponseSerializer
from .permissions import RoleBasedAccessPermission
import logging  

logger = logging.getLogger(__name__)  


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [RoleBasedAccessPermission]  # allow user signup
    
    @swagger_auto_schema(operation_description="🔓 POST: Open for user registration (no authentication required).")
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
            # This ensures all DB operations in super().create() are atomic
                response = super().create(request, *args, **kwargs)
                logger.info("User registered successfully: %s", response.data)
            return response
        #return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            if 'unique' in str(e).lower():
                raise ValidationError("A user with this email already exists.")
            raise ValidationError("An unexpected error occurred.")

    @swagger_auto_schema(operation_description="🔒 GET: Only 'admin' users can view all user accounts.")
    def list(self, request, *args, **kwargs):
        try:
           response = super().list(request, *args, **kwargs)
           logger.info("User list fetched successfully. Count: %d", len(response.data))
           return response
        except Exception as e:
            logger.error("Error fetching user list: %s", str(e), exc_info=True)
            raise APIException("Failed to retrieve records.")


    @swagger_auto_schema(operation_description="🔒 GET (detail): Only 'admin' users can view specific user details.")
    def retrieve(self, request, *args, **kwargs):
        try:
           response = super().retrieve(request, *args, **kwargs)
           logger.info("User fetched successfully.", response.data)
           return response
        except Exception as e:
            logger.error("Error fetching user: %s", str(e), exc_info=True)
            raise NotFound("User with the given ID does not exist.")

    @swagger_auto_schema(operation_description="🔒 PUT: Only 'admin' and 'staff' can fully update user profiles.")
    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
            # This ensures all DB operations in super().create() are atomic
                response = super().update(request, *args, **kwargs)
                logger.info("User updated successfully. Response: %s", response.data)
            return response
        except IntegrityError as e:
            logger.error("Integrity error during update: %s", str(e), exc_info=True)
            if 'unique' in str(e).lower():
                raise ValidationError("A user with this email already exists.")
            raise ValidationError("Failed to update user due to an internal error.")
        except Exception as e:
            logger.error("Error updating user: %s", str(e), exc_info=True)
            raise NotFound("User to update not found.")
        #return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="🔒 PATCH: Only 'admin' and 'staff' can partially update user profiles.")
    def partial_update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
            # This ensures all DB operations in super().create() are atomic
                response = super().partial_update(request, *args, **kwargs)
                logger.info("User partially updated successfully. Response: %s", response.data)
            return response
        except IntegrityError as e:
            logger.error("Integrity error during partial update: %s", str(e), exc_info=True)
            if 'unique' in str(e).lower():
                raise ValidationError("A user with this email already exists.")
            raise ValidationError("Failed to partially update user due to an internal error.")
        except Exception as e:
            logger.error("Error partial updating user: %s", str(e), exc_info=True)
            raise NotFound("User to partial update not found.")
       # return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="🔒 DELETE: Only 'admin' users can delete user accounts.")
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
            # This ensures all DB operations in super().create() are atomic
                response = super().destroy(request, *args, **kwargs)
                logger.info("User deleted successfully: ID %s", kwargs.get('pk'))
            return response
        except Exception as e:
             logger.error("Error deleting user ID %s: %s", kwargs.get('pk'), str(e), exc_info=True)
             raise NotFound("User to delete not found.")
        #return super().destroy(request, *args, **kwargs)
    

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [RoleBasedAccessPermission]
    
    @swagger_auto_schema(operation_description="🔓 GET: Accessible to all authenticated users.")
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            logger.info("Book list fetched successfully. Count: %d", len(response.data))
            return response
        except Exception as e:
            logger.error("Error fetching book list: %s", str(e), exc_info=True)
            raise APIException("Failed to retrieve records.")

    @swagger_auto_schema(operation_description="🔒 POST: Only 'admin' users can create a book.")
    def create(self, request, *args, **kwargs):
        try:
           with transaction.atomic():
            # This ensures all DB operations in super().create() are atomic
                response = super().create(request, *args, **kwargs)
                logger.info("Book registered successfully: %s", response.data)
           return response
        except IntegrityError as e:
            if 'unique' in str(e).lower():
                raise ValidationError("A book with this title and author already exists.")
            raise ValidationError("An unexpected error occurred.")
        #return super().create(request, *args, **kwargs)
        
    @swagger_auto_schema(operation_description="🔒 GET (detail): Only 'admin' users can view specific book details.")
    def retrieve(self, request, *args, **kwargs):
        try:
           response = super().retrieve(request, *args, **kwargs)
           logger.info("Book fetched successfully.", response.data)
           return response
        except Exception as e:
           logger.error("Error fetching book: %s", str(e), exc_info=True)
           raise NotFound("Book with the given ID does not exist.")

    @swagger_auto_schema(operation_description="🔒 PUT: Only 'admin' and 'staff' users can update a book.")
    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # This ensures all DB operations in super().create() are atomic
                    response = super().update(request, *args, **kwargs)
                    logger.info("Book updated successfully: %s", response.data)
            return response
        except IntegrityError as e:
            logger.error("Integrity error during update: %s", str(e), exc_info=True)
            if 'unique' in str(e).lower():
                raise ValidationError("A book with this title and author already exists.")
            raise ValidationError("Failed to update book due to an internal error.")
        except Exception as e:
            logger.error("Error updating book: %s", str(e), exc_info=True)
            raise NotFound("Book to update not found.")
        
        #return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="🔒 PATCH: Only 'admin' and 'staff' users can partially update a book.")
    def partial_update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # This ensures all DB operations in super().create() are atomic
                    response = super().partial_update(request, *args, **kwargs)
                    logger.info("Book partial updated successfully: %s", response.data)
            return response
        except IntegrityError as e:
            logger.error("Integrity error during partial update: %s", str(e), exc_info=True)
            if 'unique' in str(e).lower():
                raise ValidationError("A book with this title and author already exists.")
            raise ValidationError("Failed to partially update book due to an internal error.")
        except Exception as e:
            logger.error("Error partial updating book: %s", str(e), exc_info=True)
            raise NotFound("Book to partial update not found.")
        #return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="🔒 DELETE: Only 'admin' users can delete a book.")
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # This ensures all DB operations in super().create() are atomic
                    response = super().destroy(request, *args, **kwargs)
                    logger.info("Book deleted successfully: ID %s", kwargs.get('pk'))
            return response
        except Exception as e:
            logger.error("Error deleting book ID %s: %s", kwargs.get('pk'), str(e), exc_info=True)
            raise NotFound("Book to delete not found.")
        #return super().destroy(request, *args, **kwargs)
    
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [RoleBasedAccessPermission]
    
    @swagger_auto_schema(operation_description="🔓 GET: All roles can view products.")
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            logger.info("Product list fetched successfully. Count: %d", len(response.data))
            return response
        except Exception as e:
            logger.error("Error fetching product list: %s", str(e), exc_info=True)
            raise APIException("Failed to retrieve records.")

    @swagger_auto_schema(operation_description="🔒 POST: Only admin can create a product.")
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # This ensures all DB operations in super().create() are atomic
                    response = super().create(request, *args, **kwargs)
                    logger.info("Product registered successfully: %s", response.data)
            return response
        except IntegrityError as e:
            if 'unique' in str(e).lower():
                raise ValidationError("A product with this SKU already exists.")
            raise ValidationError("An unexpected error occurred.")
        #return super().create(request, *args, **kwargs)
        
    @swagger_auto_schema(operation_description="🔒 GET (detail): Only 'admin' users can view specific product details.")
    def retrieve(self, request, *args, **kwargs):
        try:
           response = super().retrieve(request, *args, **kwargs)
           logger.info("Product fetched successfully.", response.data)
           return response
        except Exception as e:
           logger.error("Error fetching product: %s", str(e), exc_info=True)
           raise NotFound("Product with the given ID does not exist.")
    
    @swagger_auto_schema(operation_description="🔒 PUT: Only 'admin' and 'staff' users can update a book.")
    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # This ensures all DB operations in super().create() are atomic
                    response = super().update(request, *args, **kwargs)
                    logger.info("Product updated successfully: %s", response.data)
            return response
        except IntegrityError as e:
            logger.error("Integrity error during update: %s", str(e), exc_info=True)
            if 'unique' in str(e).lower():
                raise ValidationError("A product with this SKU already exists.")
            raise ValidationError("Failed to update product due to an internal error.")
        except Exception as e:
            logger.error("Error updating product: %s", str(e), exc_info=True)
            raise NotFound("Product to update not found.")
        #return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="🔒 PATCH: Only 'admin' and 'staff' users can partially update a book.")
    def partial_update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # This ensures all DB operations in super().create() are atomic
                    response = super().partial_update(request, *args, **kwargs)
                    logger.info("Product partial updated successfully: %s", response.data)
            return response
        except IntegrityError as e:
            logger.error("Integrity error during partial update: %s", str(e), exc_info=True)
            if 'unique' in str(e).lower():
                raise ValidationError("A product with this SKU already exists.")
            raise ValidationError("Failed to partially update product due to an internal error.")
        except Exception as e:
            logger.error("Error partial updating product: %s", str(e), exc_info=True)
            raise NotFound("Product to partial update not found.")
        #return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="🔒 DELETE: Only 'admin' users can delete a book.")
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # This ensures all DB operations in super().create() are atomic
                    response = super().destroy(request, *args, **kwargs)
                    logger.info("Product deleted successfully: ID %s", kwargs.get('pk'))
            return response
        except Exception as e:
            logger.error("Error deleting product ID %s: %s", kwargs.get('pk'), str(e), exc_info=True)
            raise NotFound("Product to delete not found.")
        #return super().destroy(request, *args, **kwargs)


class LogoutView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logout user by invalidating token",
        responses={200: LogoutResponseSerializer()}
    )
    def create(self, request):
        _ = request 
        # your logout logic
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
 
 

