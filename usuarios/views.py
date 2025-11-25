from django.shortcuts import render
from django.http import JsonResponse
from usuarios.models import Usuario


def home(request):
    """
    Rota principal da API, retorna uma mensagem de boas-vindas
    e a versão da API.
    """
    return JsonResponse({
        'mensagem': "Bem vindo ao Geovanni's Pizza - Django Version",
        'versao': '1.0'
    })


def listar_usuarios(request):
    # Passo 1: ir no banco e trazer os usuarios
    
	usuarios = Usuario.objects.all()
	dados = []
	for usuario in usuarios:
		dados.append({
			'id': usuario.id,
			'nome': usuario.nome,
			'email': usuario.email,
			'criado':usuario.criado.isoformat()
		})
            
	return JsonResponse({
		'usuarios': dados,
		'total': len(dados)
	})

# listar usuarios usando filtros
def listar_usuarios_com_filtros(request):

	# 1 passo - pegar todos os usuarios
	usuarios = Usuario.objects.all()

	# 2 passo - filtrar por email
	# 2.1 - pegar o email da URL
	email_consulta = request.GET.get('email')

	if email_consulta:
		usuarios = usuarios.filter(
			email__icontains=email_consulta
		)
	
	nome_consulta = request.GET.get('nome')
	if nome_consulta:
		usuarios = usuarios.filter(
			nome__icontains=nome_consulta
		)

	ordem = request.GET.get('ordem', '-criado')
	# segunda variavel -> formato padrão
	usuarios = usuarios.order_by(ordem)

	dados = [
		{
			'id':usuario.id,
			'nome': usuario.nome,
			'email': usuario.email,
		}
		for usuario in usuarios
	]
	return JsonResponse({
		'dados':dados,
		'total': len(dados),
		'filtros':{
			'nome': nome_consulta,
			'email': email_consulta,
			'ordem': ordem
		}
	})
def buscar_usuario(request, id):
    """
    GET /usuarios/1/
    Busca um usuário específico por ID
    
    No Flask:
    @app.route('/usuarios/<int:id>')
	def buscar_usuario(id):
    	usuario = Usuario.query.get(id)
    """
    
    try:
        usuario = Usuario.objects.get(id=id)
        
        dados = {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'criado': usuario.criado.isoformat(),
            'atualizado': usuario.atualizado.isoformat()
        }
        
        return JsonResponse(dados)
        
    except Usuario.DoesNotExist:
        return JsonResponse(
            {'erro': 'Usuário não encontrado'},
            status=404
        )

