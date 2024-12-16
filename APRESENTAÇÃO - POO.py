class Mensagem:
    def __init__(self, conteudo, tipo, remetente, destinatario, id):
        self.id = id
        self.tipo = tipo
        self.conteudo = conteudo
        self.remetente = remetente
        self.destinatario = destinatario

    def __str__(self):
        return f"Mensagem {self.id} de {self.remetente} para {self.destinatario}: {self.conteudo}"

class DispositivoMovel:
    def __init__(self, id):
        self.id = id
        self.mensagens_recebidas = []
        self.ligacao_ativa = False

    def enviar_mensagem(self, conteudo, destinatario, tipo, estacao_base):        
        mensagem = Mensagem(conteudo, tipo, f"Dispositivo {self.id}", destinatario, len(self.mensagens_recebidas) + 1)
        print(f"Dispositivo {self.id} enviou mensagem: {mensagem}")
        estacao_base.receber_mensagem(mensagem)

    def receber_mensagem(self, mensagem):
        print(f"Dispositivo{self.id} recebeu mensagem {mensagem}")
        self.mensagens_recebidas.append(mensagem)

    def iniciar_ligacao(self, algum_dispositivo):
        print(f"Dispositivo{self.id} iniciou ligação com Dispositivo{algum_dispositivo.id}")
        algum_dispositivo.receber_ligacao(self)

    def receber_ligacao(self, remetente_dispositivo):
        resposta = input(f"Dispositivo{self.id} recebeu ligação de Dispositivo{remetente_dispositivo.id}. Deseja atender? (sim ou não)")
        if resposta == "sim":
            print(f"Dispositivo{self.id} atendeu ligação de Dispositivo{remetente_dispositivo.id}")
            self.ligacao_ativa = True
            self.dispositivo_em_ligacao = remetente_dispositivo
        else:
            print(f"Dispositivo{self.id} recusou ligação de Dispositivo")

    def  conversa(self, remetente_dispositivo):
        print(f"Dispositivo{self.id} está em ligação com Dispositivo{remetente_dispositivo.id}")
        input("Digite sair para encerrar a ligação")
        self.encerrar_ligacao(remetente_dispositivo)

    def encerrar_ligacao(self, remetente_dispositivo):
        print(f"Dispositivo{self.id} encerrou a ligação com Dispositivo{remetente_dispositivo.id}")
        self.ligacao_ativa = False  
    
class EstacaoBase:
    def __init__(self, id):
        self.id = id
        self.buffer = []

    def receber_mensagem(self,mensagem):
        print(f"Estação Base{self.id} recebeu mensagem{mensagem}")
        self.buffer.append(mensagem)

    def enviar_mensagem(self, destinatario):
        if self.buffer:
            mensagem = self.buffer.pop(0)
            print(f"Estação Base {self.id} enviou mensagem para Dispositivo {destinatario.id}: {mensagem}")
            destinatario.receber_mensagem(mensagem)
        else:
            print(f"Estação Base {self.id} não possui mensagens para enviar")
                

class RedeCentral:
    def __init__(self):
        self.historico = []

    def receber_mensagem(self, mensagem):
        print(f"Rede Central recebeu mensagem{mensagem}")
        self.historico.append(mensagem)
        self.encaminhar_mensagem(mensagem)

    def encaminhar_mensagem(self, mensagem):
        if mensagem.tipo == "SMS":
            print(f"Rede Central encaminhou mensagem{mensagem.conteudo} para o destinatario{mensagem.destinatario}")
        else:
            print(f"Ligação iniciada{mensagem.conteudo} para o destinatario{mensagem.destinatario}")    

if __name__ == "__main__":
    pass

