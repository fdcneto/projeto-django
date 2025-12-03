from rest_framework import viewsets, status

# esse import é como vamos usar a rota
from rest_framework.response import Response

# esse import é como vamos dar a resposta
from rest_framework.decorators import action

# esse import é para criar rotas extras
from rest_framework.permissions import AllowAny

# esse import mexe com permissões
# (quem pode usar as rotas)


from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer, LoginSerializer, CadastroSerializer


class UsuarioViewSets(viewsets.ModelViewSet):
    # apresente o modelo do banco, junto com
    # todas as entradas (todos os objetos)
    queryset = Usuario.objects.all()
    # regras do jogo: quais restrições que cada
    # rota irá ter
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]

    # criar rotas extras -> ideia de usuarios/rota

    # action de cadastro (não é necessario,
    # mas fica mais organizado)

    @action(detail=False, methods=["post"], url_path="cadastro")
    def cadastro(self, request):
        # passando os dados do cadastro para
        # o serializer validar
        serializer = CadastroSerializer(data=request.data)

        if serializer.is_valid():
            # cadastrar -> criar o usuario no banco
            usuario = serializer.save()
            return Response(
                {
                    "mensagem": "Usuario cadastrado com sucesso",
                    "usuario": UsuarioSerializer(usuario).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response({"erro": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
