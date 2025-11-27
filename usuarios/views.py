from rest_framework.views import APIView
# esse import é como vamos usar a rota
from rest_framework.response import Response
# esse import é como vamos dar a resposta
from rest_framework import status
# status da resposta
from django.shortcuts import get_object_or_404

from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer

class UsuarioListAPIView(APIView):
	"""
	GET - Listar usuários
	POST - Criar novo usuário
	"""
	def get(self, request):
		
		usuarios = Usuario.objects.all()		
		serializer = UsuarioSerializer(usuarios, many=True)
		return Response({
			'dados': serializer.data,
			'total': len(serializer.data)
		})
	
	def post(self, request):
		
		# passo 1: receber/analisar os dados
		serializer = UsuarioSerializer(data=request.data)
		# desserializar os dados (JSON -> objeto Python)
		# valida
		if serializer.is_valid():
			Usuario = serializer.save()
			# passo 2: salvar no banco
			return Response({
				'mensagem': 'Usuário criado com sucesso!',
				'usuario': UsuarioSerializer(Usuario).data
		}, status=status.HTTP_201_CREATED)

		# se foi inválido, retorno o erro
		return Response({
			'erros': serializer.errors
		}, status=status.HTTP_400_BAD_REQUEST)
	



		class UsuarioDetalhesAPIView(APIView):

			"""
			GET - Buscar um usuário
			PATCH - Atualizar um usuário
			delete - Deletar um usuário
			"""	
			def get_object(self, id):
				return get_object_or_404(Usuario, id=id)
			
			def get(self, request, id):
				usuario = self.get_object(id)
				serializer = UsuarioSerializer(usuario)
				return Response(serializer.data)
			
				



			def patch(self, request, id):
				usuario = self.get_object(id)
				serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
				if serializer.is_valid():
					serializer.save()
					return Response({
						'mensagem': 'Usuário atualizado com sucesso',
						'usuario': serializer.data
					}, status=status.HTTP_200_OK)
				return Response({
					'erros': serializer.errors
				}, status=status.HTTP_400_BAD_REQUEST)
						