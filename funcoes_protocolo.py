def encapsular(remetente, comando, dados):
    tamanho = 2+16+8+len(dados)
    #ajustando o tamnho maximo do remetente
    if len(remetente)<16:
        remetente_ajustado = remetente + ((16-len(remetente))*'?')
    else:
        remetente_ajustado = remetente[0:16]
    #ajustando o tamnho maximo do comando
    if len(comando)<8:
        comando_ajustado = comando + ((8-len(comando))*'?')
    else:
        comando_ajustado = comando[0:8]
    
    mensagem_encapsulada = (str(tamanho) + remetente_ajustado + comando_ajustado + dados).encode('utf-8')
    return mensagem_encapsulada

#metodo para desencapsulamento da mensagem
def desencapsular(mensagem):
    mensagem_desencapsulada = mensagem.decode('utf-8')
    tamanho_desencapsulado = int(mensagem_desencapsulada[0:2])
    remetente = mensagem_desencapsulada[2:18]
    comando = mensagem_desencapsulada[18:26]
    dados_desencapsulado = mensagem_desencapsulada[26:]
    remetente_desencapsulado = remetente.strip('?')
    comando_desencapsulado = comando.strip('?')

    return tamanho_desencapsulado, remetente_desencapsulado, comando_desencapsulado, dados_desencapsulado
