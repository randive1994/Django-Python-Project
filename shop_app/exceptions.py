from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        logger.error(f"Error occurred: {exc} in {context['view']}")
        # Customize the default response structure
        customized_response = {
            'status_code': response.status_code,
            'error': True,
            'message': response.data,
        }
        return Response(customized_response, status=response.status_code)

    # If DRF didn't handle it, return a generic 500
    return Response({
        'status_code': 500,
        'error': True,
        'message': 'Internal server error',
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
