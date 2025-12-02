from rest_framework import serializers
from usuarios.models import Usuario

class UsuarioSerializer(
    serializers.ModelSerializer):
    # "equivale" ao to_dict do Flask 
    # (só que mais poderoso)

    senha = serializers.CharField(
        min_length=8,
        max_length=50,
        write_only=True # Não aparece na saida
    )
    senha_confirmacao = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = Usuario # Qual modelo vai serializar
        fields = ['id', 'nome', 'email', 'senha',
            'criado', 'atualizado', 'senha_confirmacao']
        
        # todas as colunas do banco
        # fields = '__all__'

        # se quisesse pegar varias colunas
        # exceto algumas
        # exclude = ['senha']

        # Informar os campos de apenas leitura
        # Não podem ser modificados
        read_only_fields = ['id', 'criado',
                      'atualizado']
    
    def validate_nome(self, value):
        # validar o campo nome
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError(
                'Nome deve ter no mínimo 3 ' \
                'caracteres'
            )
        return value
    
    def validate_email(self, value):
        email_criacao = value.lower().strip()
        # verificar se o email existe
        if Usuario.objects.filter(
            email=email_criacao).exists():
            raise serializers.ValidationError(
                'Este email já está cadastrado'
            )
        return email_criacao
    
    def validate_senha(self, value):
        if value.isdigit():
            raise serializers.ValidationError(
                'Senha não pode ser apenas números'
            )
        return value
    
    def validate(self, data):

        senha = data.get('senha')
        senha_confirmacao = \
        data.get('senha_confirmacao')

        if senha != senha_confirmacao:
            raise serializers.ValidationError({
                'senha_confirmacao':
                'As senhas não coincidem'
            })
        # remover o que não faz parte do modelo
        data.pop('senha_confirmacao')
        return data

    def update(self, instance, validated_data):
        '''
        Ao atualizar, verifica se a senha é diferente 
        '''

        if 'senha' in validated_data:
            if instance.verificar_senha(
                validated_data['senha']):
                # chamar o metodo verificar_senha do modelo
                # e passar a senha digitada
                raise serializers.ValidationError({
                    'senha': 'Nova senha não '\
                    'pode ser igual a anterior'
                })
        # atualizar senha do usuario
        for campo, valor in validated_data.items():
            setattr(instance, campo, valor)
        instance.save()
        return instance
    








    class LoginSerializer(serializers.Serializer):
        



    email = serializers.EmailField(required=True)
    senha = serializers.CharField(
        required=True, 
        write_only=True, 
        style={'input_type': 'password'}
    )
    def validate(self, data):
    email_login = data.get('email').lower().strip()
    senha_login = data.get('senha')
    
    
    
    
    
    