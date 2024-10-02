from django.conf import settings
import pandas as pd
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from groq import Groq

from .serializers import FileUploadSerializer

client = Groq(api_key=settings.GROQ_API_KEY)

def handle_review(df):
   
    df_json = df.to_json(orient='records') 


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Process the given dataframe: {df_json}",
            }
        ],
        model="gemma-7b-it",
        temperature=0.5,
        max_tokens=8000,
        top_p=1,
        stop=None,
        stream=False,
    )

    response_content = chat_completion.choices[0].message.content

    print(response_content)

    return response_content
        

class FileUploadView(APIView):
    def post(self,request):
        serializer=FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file=serializer.validated_data['file']
            df = self.handle_uploaded_file(file)
            scores=handle_review(df=df)
            return Response(scores,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)

    def handle_uploaded_file(self, file):
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        return df
    
    

    
