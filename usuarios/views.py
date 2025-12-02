from rest_framework import viewsets
# esse import é como vamos usar a rota
from rest_framework.response import Response
# esse import é como vamos dar a resposta

from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
	# apresente o modelo do banco, junto com
	# todas as entradas (todos os objetos)
	queryset = Usuario.objects.all()
	# regras do jogo: quais restrições que cada rota irá ter
	serializer_class = UsuarioSerializer
	

	"""
	GET - listar usuarios
	POST - Criar novo usuario
	"""
	def get(self, request):

		usuarios = Usuario.objects.all()
		serializer = UsuarioSerializer(usuarios, many=True)
		return Response({
			'dados': serializer.data,
			'total': len(serializer.data)
		})
	
	def post(self, request):

		# Passo 1 - receber/analisar os dados
		serializer = UsuarioSerializer(
			data=request.data
		)
		# Desserializar (JSON -> Python)
		# valida
		if serializer.is_valid():
			usuario = serializer.save()

			return Response({
				'mensagem': 'Usuário criado com sucesso',
				'usuario': UsuarioSerializer(usuario).data
			}, status=status.HTTP_201_CREATED)
		
		# se foi inválido, retorno o erro
		return Response({
			'erro':serializer.errors
		}, status=status.HTTP_400_BAD_REQUEST)


class UsuarioDetalhesAPIView(APIView):
	"""
	GET 	- Buscar um usuario\n
	PATCH 	- Atualizar \n
	DELETE 	- Deletar\n
	"""
	# função auxiliar para pegar o usuario
	def get_object(self, id_usuario):
		return get_object_or_404(
			Usuario, id=id_usuario)
	
	def get(self, request, id):
		usuario = self.get_object(id)
		serializer = UsuarioSerializer(usuario)

		return Response(serializer.data)
	
	def patch(self, request, id):
		usuario = self.get_object(id)
		# 1 -> passa o usuario
		# 2 -> passa o(s) campo(s) mudado(s)





		# 3 -> avisa que pode atualizar só parte
		serializer = UsuarioSerializer(
			usuario,
			data=request.data,
			partial=True
		)
		# validar
		if serializer.is_valid():
			serializer.save()
			return Response({
				'mensagem': 'Usuário atualizado com sucesso',
				'usuario': serializer.data
			}, status=status.HTTP_200_OK)
		
		# caminho triste - falhou atualização
		return Response(
			serializer.errors,
			status=status.HTTP_400_BAD_REQUEST
		)

