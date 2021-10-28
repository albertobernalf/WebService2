from django.shortcuts import render
from rest_framework import serializers, viewsets, routers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from reportes.models import User
from django.http import HttpResponse, JsonResponse
import MySQLdb
from reportlab.lib.fonts import addMapping
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.platypus import *
from reportlab.lib.units import cm
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow
)
import json
import io


# Create your views here.


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff']


# class UserApiView(APIView):
@api_view(['GET', 'POST'])
def user_api_view(request):
    #    def get(self, request):
    if request.method == 'GET':

        print("pase")
        queryset = User.objects.all()
        user_serializer = UserSerializer(queryset, many=True)
        print("pase")
        return Response(user_serializer.data)

    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_detail_view(request, pk=None):
    #    def get(self, request):
    if request.method == 'GET':
        user = User.objects.filter(id=pk).first()
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

    elif request.method == 'PUT':
        user = User.objects.filter(id=pk).first()
        user_serializer = UserSerializer(user, data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)

    elif request.method == 'DELETE':
        user = User.objects.filter(id=pk).first()
        user.delete()
        return Response("Eliminado")

    return Response(user_serializer.errors)


def reportes_view(request):
    Story = []
    buff = io.BytesIO()
    doc = SimpleDocTemplate(buff, pagesize=letter, rightMargin=26, leftMargin=32, topMargin=72, bottomMargin=18)

    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.align = 'CENTER'
    styleBH.fontSize = 6

    estilos = getSampleStyleSheet()

    headline_mayor = estilos["Heading1"]
    headline_mayor.alignment = TA_LEFT
    headline_mayor.leading = 8
    headline_mayor.fontSize = 10
    headline_mayor.fontName = "Helvetica-Bold"
    headline_mayor.spaceAfter = 0
    headline_mayor.spaceBefore = 0

    headline_mayor1 = estilos["Heading5"]
    headline_mayor1.alignment = TA_LEFT
    headline_mayor1.leading = 6
    headline_mayor1.fontSize = 8
    headline_mayor1.fontName = "Helvetica-Bold"
    headline_mayor1.spaceAfter = 0
    headline_mayor1.spaceBefore = 0

    headline_mayor2 = estilos["Heading5"]
    headline_mayor2.alignment = TA_LEFT
    headline_mayor2.leading = 7
    headline_mayor2.fontSize = 8
    headline_mayor2.fontName = "Helvetica-Bold"
    headline_mayor2.spaceAfter = 0
    headline_mayor2.spaceBefore = 0

    headline_mayor3 = estilos["Heading5"]
    headline_mayor3.alignment = TA_CENTER
    headline_mayor3.leading = 8
    headline_mayor3.fontSize = 10
    headline_mayor3.fontName = "Helvetica-Bold"
    headline_mayor3.spaceAfter = 0
    headline_mayor3.spaceBefore = 0

    headline_mayor33 = estilos["Heading5"]
    headline_mayor33.alignment = TA_CENTER
    headline_mayor33.leading = 3
    headline_mayor33.fontSize = 10
    headline_mayor33.fontName = "Helvetica-Bold"
    headline_mayor33.spaceAfter = 0
    headline_mayor33.spaceBefore = 0

    headline_mayor4 = estilos["Heading5"]
    headline_mayor4.alignment = TA_CENTER
    # headline_mayor4.leftIndent= 10
    headline_mayor4.leading = 7
    headline_mayor4.fontSize = 9
    headline_mayor4.fontName = "Helvetica-Bold"
    headline_mayor4.spaceAfter = 0
    headline_mayor4.spaceBefore = 0

    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="Historia.pdf"'
    response['Content-Disposition'] = 'attachment; filename="albertoWebService.pdf"'


    myConexion = MySQLdb.connect(host='localhost', user='root', passwd='', db='user')
    cur = myConexion.cursor()
    cur.execute("SELECT id, url, username, email, is_staff   FROM reportes_user order by id")
    Usuarios = []

    for id, url, username, email, is_staff in cur.fetchall():
        Usuarios.append({'id': id, 'url': url, 'username': username, 'email': email, 'is_staff': is_staff})
        texto1 = '_______________________________________________________________________________________________'
        Story.append(Paragraph(texto1, headline_mayor))

        tbl_data1 = [
            [Paragraph("SEDE DE ATENCION:", headline_mayor3), Paragraph("001", headline_mayor3),
             Paragraph(str(url), headline_mayor3),
             Paragraph("Username:", headline_mayor), Paragraph(str(username) + 'username', headline_mayor3),
             Paragraph("", headline_mayor3),
             Paragraph("email:", headline_mayor), Paragraph(str(email) + 'email', headline_mayor3),
             Paragraph("", headline_mayor3),
             ]]

        tbl = Table(tbl_data1, colWidths=[5 * cm, 2 * cm, 6 * cm, 2 * cm, 2 * cm, 3.8 * cm])

        Story.append(tbl)

        logotipo = "C:\\EntornosPython\\WebService2\\Webservice2\\static\\images\\logo.jpg"
        imagen = Image(logotipo, 1 * inch, 1 * inch)
        Story.append(imagen)

        tbl_data = [
            [Paragraph(str(imagen), headline_mayor3), Paragraph("FUNDACION HOSPITAL SAN CARLOS:", headline_mayor3), ],
        ]

        tbl = Table(tbl_data, colWidths=[2.05 * cm, 17 * cm])

        Story.append(tbl)
        Story.append(Spacer(1, 2))
        nit = '860007373-4'
        Story.append(Paragraph(nit, headline_mayor3))
        Story.append(Spacer(1, 4))

    context  = {}
    myConexion.close()
    context['Usuarios'] = Usuarios

    print(Usuarios)
    doc.build(Story)
    response.write(buff.getvalue())
    buff.close()
    #return response
    # send file
    obj_formato = models.FormatoManual.objects.get(nombre_formato=nombre_formato)

    response = FileResponse(response, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{0}.pdf"'.format(obj_formato.nombre_formato)
    return response

    return Response(response)

