import pandas as pd
from phonenumbers import parse as parse_phone_number
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import JduUser
from django.db import IntegrityError


def join_student(request):
    # Assuming you have a Google Sheet shared publicly, you can get its CSV link
    google_sheet_url = "https://docs.google.com/spreadsheets/d/19FE14YCLIra1rPff28kxczq656A7ZvEkgHx7xzgCm0s/edit?pli=1#gid=0"
    df = pd.read_csv(google_sheet_url)


class YourView(APIView):

    def get(self, request):
        google_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRC2uz_yKytW9-nxWsipY47Eo35C01JK5tBXPA72qCVMt9CjtnXouoxU4JXmdWqKznK4s01maP_huiO/pub?gid=0&single=true&output=csv"
        df = pd.read_csv(google_sheet_url)
        result = {}
        number = 1
        for index, row in df.iterrows():
            jdu_id = int(row['ID'])
            password = row['Parol']
            name = row['ismi']
            surname = row['fam']
            phone_num = parse_phone_number(row['Tel'], region='UZ') if not pd.isnull(row['Tel']) else None
            exam_score = row['Bali']
            prents_phone_num = parse_phone_number(row['ota-onasi nomer']) if not pd.isnull(
                row['ota-onasi nomer']) else None
            address = row["Uy manzili (to'liq)"] if not pd.isnull("Uy manzili (to'liq)") else None

            # print(jdu_id, password, name, surname, phone_num)
            user_data = {'jdu_id': jdu_id, 'password': password, 'name': name, 'surname': surname,
                         'phone_num': str(phone_num),
                         "exam_score": exam_score, 'prents_phone_num': str(prents_phone_num), "address": str(address)}

            try:
                user, created = JduUser.objects.get_or_create(jdu_id=jdu_id, defaults=user_data)

                if not created:
                    # Update existing user data if needed
                    user.name = name
                    # Update other fields...
                    user.save()

                result[jdu_id] = {'status': 'success', 'message': 'User created/updated successfully'}
            except IntegrityError:
                result[jdu_id] = {'status': 'error', 'message': 'IntegrityError: Duplicate entry'}

            result[number] = user_data
            number += 1
        return Response(result, status=status.HTTP_200_OK)
