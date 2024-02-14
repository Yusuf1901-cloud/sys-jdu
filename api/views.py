import pandas as pd
from phonenumbers import parse as parse_phone_number
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import JduUser
from django.db import IntegrityError
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        jdu_id = request.data.get('jdu_id')

        password = request.data.get('password')

        if not jdu_id or not password:
            return Response({'detail': 'Both jdu_id and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Attempting login for jdu_id: {jdu_id}, password: {password}")

        user = authenticate(request, jdu_id=jdu_id, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            jdu_user_data = {
                'jdu_id': user.jdu_id,
                'name': user.name,
                'surname': user.surname,
                'phone_num': str(user.phone_num),
                'exam_score': user.exam_score,
                'parents_phone_num': str(user.parents_phone_num),
                'address': str(user.address),
            }

            response_data = {
                'token': token.key,
                'jdu_user_data': jdu_user_data,
            }

            print("Login successful")
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            print("Invalid jdu_id or password.")
            return Response({'detail': 'Invalid jdu_id or password.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)


def join_student(request):
    google_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRC2uz_yKytW9-nxWsipY47Eo35C01JK5tBXPA72qCVMt9CjtnXouoxU4JXmdWqKznK4s01maP_huiO/pub?gid=0&single=true&output=csv"
    df = pd.read_csv(google_sheet_url)
    result = {}
    for index, row in df.iterrows():
        jdu_id = int(row['ID'])
        password = row['Parol']
        name = row['ismi']
        surname = row['fam']
        phone_num = parse_phone_number(row['Tel'], region='UZ') if not pd.isnull(row['Tel']) else None
        exam_score = row['Bali']
        quote = row['Kvota']
        parents_phone_num = parse_phone_number(row['ota-onasi nomer']) if not pd.isnull(
            row['ota-onasi nomer']) else None
        address = row["Uy manzili (to'liq)"] if not pd.isnull("Uy manzili (to'liq)") else None

        # print(jdu_id, password, name, surname, phone_num)
        user_data = {'jdu_id': jdu_id, 'password': password, 'name': name, 'surname': surname,
                     'phone_num': str(phone_num),
                     "exam_score": exam_score,
                     'quote': quote,
                     'parents_phone_num': str(parents_phone_num), "address": str(address)}

        try:
            user, created = JduUser.objects.get_or_create(jdu_id=jdu_id, defaults=user_data)
            
            user = User.objects.create_user(username=jdu_id, password=password)
            user.is_active = True  # Set is_active to True explicitly
            user.save()
            
            if not created:
                # Update existing user data if needed
                user.name = name
                # Update other fields...
                user.save()

            result[jdu_id] = {'status': 'success', 'message': 'User created/updated successfully'}
        except IntegrityError:
            result[jdu_id] = {'status': 'error', 'message': 'IntegrityError: Duplicate entry'}

    return result


class YourView(APIView):

    def get(self, request):
        join_student(request)  # o'chiriladi
        jdu_users = JduUser.objects.all()

        result = {}
        number = 1

        for user in jdu_users:
            jdu_id = user.jdu_id
            password = user.password  # Note: Storing passwords in plaintext is not recommended. Use it for demonstration purposes only.
            name = user.name
            surname = user.surname
            phone_num = user.phone_num
            parents_phone_num = user.parents_phone_num
            address = user.address
            exam_score = user.exam_score
            kvota = user.quote

            user_data = {
                'jdu_id': jdu_id,
                'password': password,
                'name': name,
                'surname': surname,
                'phone_num': str(phone_num),
                'exam_score': exam_score,
                'quote': kvota,
                'parents_phone_num': str(parents_phone_num),
                'address': str(address),
            }

            # print(jdu_id, password, name, surname, phone_num)
            user_data = {'jdu_id': jdu_id, 'password': password, 'name': name, 'surname': surname,
                         'phone_num': str(phone_num),
                         "exam_score": exam_score,
                         'quote': kvota,
                         'parents_phone_num': str(parents_phone_num), "address": str(address)}

            result[number] = user_data
            number += 1
        return Response(result, status=status.HTTP_200_OK)
