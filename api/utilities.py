import bcrypt
import uuid
import hmac
import hashlib
import base64
import json
import datetime
from django.conf import settings


# Generate Refresh Token
def gen_rt() -> bytes:
    return base64.urlsafe_b64encode((str(uuid.uuid4()) + str(datetime.datetime.now())).encode()).rstrip(b'=')


# Generate Access Token (JWT)
def gen_jwt(user, payload=None) -> bytes:
    header = {
        "alg": "HS512",
        "typ": "JWT"
    }

    # If no payload provided, use default payload
    if not payload:
        payload = {
            "user_id": user.pk,
            "iat": (datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()
        }

    # Create signature using HMAC-SHA512
    h_coded = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).rstrip(b'=')
    p_coded = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).rstrip(b'=')
    unsignedToken = h_coded + b'.' + p_coded
    signature = hmac.new(settings.SECRET_KEY.encode(), msg=unsignedToken, digestmod=hashlib.sha512).digest()

    # Return constructed JWT
    return h_coded + b'.' + p_coded + b'.' + base64.urlsafe_b64encode(signature).rstrip(b'=')


# Hash Refresh Token using bcrypt
def hash_rt(rt: bytes) -> bytes:
    return bcrypt.hashpw(rt, settings.RT_BCRYPT_SALT)
