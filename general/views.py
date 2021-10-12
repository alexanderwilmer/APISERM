 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser

import json
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.models import User, Group

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import *
from solicitudes.models import *

