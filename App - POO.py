from enum import Enum
import tkinter as tk
from tkinter import messagebox

# Enum para definir os tipos de mensagem
class TipoMensagem(Enum):
    SMS = "SMS"  # Tipo de mensagem SMS
    LIGACAO = "Ligação"  # Tipo de mensagem de ligação

# Classe para representar uma mensagem
class Mensagem:
    def __init__(self, conteudo, tipo: TipoMensagem, remetente, destinatario, id):
        self.id = id  # ID da mensagem
        self.tipo = tipo  # Tipo da mensagem (SMS ou Ligação)
        self.conteudo = conteudo  # Conteúdo da mensagem
        self.remetente = remetente  # Remetente da mensagem
        self.destinatario = destinatario  # Destinatário da mensagem

    def __str__(self):
        # Representação em string da mensagem
        return f"Mensagem {self.id} de {self.remetente} para {self.destinatario}: {self.conteudo} ({self.tipo.value})"

# Classe para representar um dispositivo móvel
class DispositivoMovel:
    def __init__(self, id, estacao_base):
        self.id = id  # ID do dispositivo
        self.estacao_base = estacao_base  # Estação base associada ao dispositivo
        self.mensagens_recebidas = []  # Lista de mensagens recebidas
        self.ligacao_ativa = False  # Indica se uma ligação está ativa
        self.dispositivo_em_ligacao = None  # Dispositivo com o qual está em ligação

    def enviar_mensagem(self, conteudo, destinatario, tipo: TipoMensagem):        
        # Cria uma nova mensagem e a envia
        mensagem = Mensagem(conteudo, tipo, f"Dispositivo {self.id}", destinatario, len(self.mensagens_recebidas) + 1)
        print(f"Dispositivo {self.id} enviou mensagem: {mensagem}")
        self.estacao_base.receber_mensagem(mensagem)  # Envia a mensagem para a estação base

    def receber_mensagem(self, mensagem):
        # Adiciona a mensagem recebida à lista de mensagens
        print(f"Dispositivo {self.id} recebeu mensagem: {mensagem}")
        self.mensagens_recebidas.append(mensagem)

    def iniciar_ligacao(self, outro_dispositivo):
        # Inicia uma ligação com outro dispositivo
        print(f"Dispositivo {self.id} iniciou ligação com Dispositivo {outro_dispositivo.id}")
        outro_dispositivo.receber_ligacao(self)  # Notifica o outro dispositivo

    def receber_ligacao(self, remetente_dispositivo):
        # Recebe uma ligação de outro dispositivo
        resposta = messagebox.askyesno("Chamada", f"Dispositivo {self.id} recebeu ligação de Dispositivo {remetente_dispositivo.id}. Deseja atender?")
        if resposta:
            print(f"Dispositivo {self.id} atendeu ligação de Dispositivo {remetente_dispositivo.id}")
            self.ligacao_ativa = True  # Define que a ligação está ativa
            self.dispositivo_em_ligacao = remetente_dispositivo  # Armazena o dispositivo em ligação
            self.conversa(remetente_dispositivo)  # Inicia a conversa
        else:
            print(f"Dispositivo {self.id} recusou ligação de Dispositivo {remetente_dispositivo.id}")

    def conversa(self, remetente_dispositivo):
        # Mantém a conversa enquanto a ligação estiver ativa
        while self.ligacao_ativa:
            resposta = messagebox.askyesno("Chamada", f"Dispositivo {self.id} está em ligação com Dispositivo {remetente_dispositivo.id}. Deseja encerrar a ligação?")
            if resposta:
                self.encerrar_ligacao(remetente_dispositivo)  # Encerra a ligação se o usuário desejar

    def encerrar_ligacao(self, remetente_dispositivo):
        # Encerra a ligação com o dispositivo remetente
        print(f"Dispositivo {self.id} encerrou a ligação com Dispositivo {remetente_dispositivo.id}")
        self.ligacao_ativa = False  # Define que a ligação não está mais ativa
        self.dispositivo_em_ligacao = None  # Limpa o dispositivo em ligação

# Classe para representar a estação base
class EstacaoBase:
    def __init__(self, id):
        self.id = id  # ID da estação base
        self.buffer = []  # Buffer para armazenar mensagens

    def receber_mensagem(self, mensagem):
        # Recebe a mensagem e a adiciona ao buffer
        print(f"Estação Base {self.id} recebeu mensagem: {mensagem}")
        self.buffer.append(mensagem)

    def enviar_mensagem(self, destinatario):
        # Envia a primeira mensagem do buffer para o destinatário
        if self.buffer:
            mensagem = self.buffer.pop(0)  # Remove a mensagem do buffer
            print(f"Estação Base {self.id} enviou mensagem para Dispositivo {destinatario.id}: {mensagem}")
            destinatario.receber_mensagem(mensagem)  # Envia a mensagem para o dispositivo
        else:
            print(f"Estação Base {self.id} não possui mensagens para enviar")  # Mensagem se o buffer estiver vazio

# Classe para representar a interface do aplicativo
class SimuladorDispositivos:
    def __init__(self, master):
        self.master = master  # Janela principal do aplicativo
        self.master.title("Simulador de Dispositivos Móveis")  # Título da janela

        # Criação da estação base e dispositivos
        self.estacao_base = EstacaoBase(id=1)  # Cria a estação base
        self.dispositivo1 = DispositivoMovel(id=1, estacao_base=self.estacao_base)  # Cria o primeiro dispositivo
        self.dispositivo2 = DispositivoMovel(id=2, estacao_base=self.estacao_base)  # Cria o segundo dispositivo

        # Interface para o Dispositivo 1
        self.criar_interface_dispositivo(1)

        # Interface para o Dispositivo 2
        self.criar_interface_dispositivo(2)

    def criar_interface_dispositivo(self, dispositivo_id):
        # Cria a interface gráfica para um dispositivo
        label = tk.Label(self.master, text=f"Dispositivo {dispositivo_id} - Digite sua mensagem: ")
        label.pack()  # Adiciona o rótulo à janela

        entry = tk.Entry(self.master)  # Campo de entrada para mensagens
        entry.pack()  # Adiciona o campo à janela

        enviar_button = tk.Button(self.master, text="Enviar SMS", command=lambda: self.enviar_sms(dispositivo_id, entry))
        enviar_button.pack()  # Botão para enviar SMS

        chamada_button = tk.Button(self.master, text="Iniciar chamada", command=lambda: self.iniciar_chamada(dispositivo_id))
        chamada_button.pack()  # Botão para iniciar chamada

        encerrar_button = tk.Button(self.master, text="Encerrar chamada", command=lambda: self.encerrar_chamada(dispositivo_id))
        encerrar_button.pack()  # Botão para encerrar chamada

        mensagens_text = tk.Text(self.master, height=10, width=50)  # Área de texto para exibir mensagens
        mensagens_text.pack()  # Adiciona a área de texto à janela

        # Armazena referências para os dispositivos
        if dispositivo_id == 1:
            self.entry1 = entry
            self.mensagens_text1 = mensagens_text
        else:
            self.entry2 = entry
            self.mensagens_text2 = mensagens_text

    def enviar_sms(self, dispositivo_id, entry):
        # Envia uma mensagem SMS do dispositivo
        conteudo = entry.get()  # Obtém o conteúdo da mensagem
        if conteudo:
            if dispositivo_id == 1:
                self.dispositivo1.enviar_mensagem(conteudo, "Dispositivo 2", TipoMensagem.SMS)  # Envia mensagem do dispositivo 1
                self.mensagens_text1.insert(tk.END, f"Dispositivo 1 enviou: {conteudo}\n")  # Atualiza a área de texto
            else:
                self.dispositivo2.enviar_mensagem(conteudo, "Dispositivo 1", TipoMensagem.SMS)  # Envia mensagem do dispositivo 2
                self.mensagens_text2.insert(tk.END, f"Dispositivo 2 enviou: {conteudo}\n")  # Atualiza a área de texto
            entry.delete(0, tk.END)  # Limpa o campo de entrada
        else:
            messagebox.showwarning("Aviso", "Digite uma mensagem")  # Alerta se o campo estiver vazio

    def iniciar_chamada(self, dispositivo_id):
        # Inicia uma chamada entre dispositivos
        if dispositivo_id == 1:
            self.dispositivo1.iniciar_ligacao(self.dispositivo2)  # Dispositivo 1 inicia ligação com Dispositivo 2
        else:
            self.dispositivo2.iniciar_ligacao(self.dispositivo1)  # Dispositivo 2 inicia ligação com Dispositivo 1

    def encerrar_chamada(self, dispositivo_id):
        # Encerra a chamada ativa do dispositivo
        if dispositivo_id == 1:
            if self.dispositivo1.ligacao_ativa:
                self.dispositivo1.encerrar_ligacao(self.dispositivo2)  # Encerra a ligação do Dispositivo 1
                self.mensagens_text1.insert(tk.END, "Dispositivo 1 encerrou a chamada\n")  # Atualiza a área de texto
            else:
                messagebox.showwarning("Aviso", "Dispositivo 1 não está em chamada")  # Alerta se não estiver em chamada
        else:
            if self.dispositivo2.ligacao_ativa:
                self.dispositivo2.encerrar_ligacao(self.dispositivo1)  # Encerra a ligação do Dispositivo 2
                self.mensagens_text2.insert(tk.END, "Dispositivo 2 encerrou a chamada\n")  # Atualiza a área de texto
            else:
                messagebox.showwarning("Aviso", "Dispositivo 2 não está em chamada")  # Alerta se não estiver em chamada

if __name__ == "__main__":
    root = tk.Tk()  # Cria a janela principal do Tkinter
    app = SimuladorDispositivos(root)  # Inicializa o simulador de dispositivos
    root.mainloop()  # Inicia o loop principal da interface gráfica