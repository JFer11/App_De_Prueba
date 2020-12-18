import os
from itsdangerous import URLSafeTimedSerializer


serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))
