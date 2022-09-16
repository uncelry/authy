from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import Client
from .utilities import gen_rt, gen_jwt, hash_rt
import uuid


# View for generating token pair
@api_view(['POST'])
def generate_tokens_view(request):

    # User ID (UUID) is required
    try:
        user_id = request.POST['user_id']
    except KeyError:
        return Response(data='No user ID was provided', status=status.HTTP_400_BAD_REQUEST)

    # Generate and bcrypt Refresh Token
    rt = gen_rt()
    hashed_rt = hash_rt(rt).decode()

    # Get or create Client instance
    try:
        client, created = Client.objects.get_or_create(public_id=uuid.UUID(user_id), defaults={'refresh': hashed_rt})
    except ValueError:
        return Response(data='Invalid client UUID', status=status.HTTP_400_BAD_REQUEST)

    # Generate Access Token with default payload
    jwt = gen_jwt(client, payload=None)

    # Respond with token pair for a new Client instance
    if created:
        return Response(data={'jwt': jwt, 'rt': rt}, status=status.HTTP_201_CREATED)

    # Update bcrypt hash for existing Client instance and send response
    client.refresh = hashed_rt
    client.save()
    return Response(data={'jwt': jwt, 'rt': rt}, status=status.HTTP_200_OK)


# View for refreshing token pair
@api_view(['POST'])
def refresh_tokens_view(request):

    # Refresh Token is required
    try:
        rt = request.POST['rt']
    except KeyError:
        return Response(data='No Refresh token was provided', status=status.HTTP_400_BAD_REQUEST)

    # Valid Refresh Token is required
    try:
        client = Client.objects.get(refresh=hash_rt(rt.encode()).decode())
    except ObjectDoesNotExist:
        return Response(data='Invalid Refresh token', status=status.HTTP_400_BAD_REQUEST)

    # Create new Access Token
    jwt = gen_jwt(client)

    # Create new Refresh Token
    rt = gen_rt()
    hashed_rt = hash_rt(rt).decode()

    # Update bcrypt hash for Client instance and send response
    client.refresh = hashed_rt
    client.save()
    return Response(data={'jwt': jwt, 'rt': rt}, status=status.HTTP_200_OK)
