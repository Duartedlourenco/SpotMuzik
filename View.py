import tkinter as tk
import customtkinter as ctk
import pygame
from tkinter import messagebox
from Model.Utilizador import *
from Model.UtilizadorLinkedList import *
from Model.DataBase import DataBase
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from io import BytesIO


class View:
    # Inicializar pygame mixer
    pygame.mixer.init()

    def __init__(self, master):
        self.master = master
        self.utilizadores = UtilizadorLinkedList()
        self.database = DataBase()
        self.load_utilizador()
        self.master.geometry("600x500")
        self.master.title("SpotMuzik")
        self.master.configure(bg="#121212")  # Define o fundo da janela principal para preto

        self.spotify = None
        self.token_info = None
        self.utilizador_login = None
        self.playlists = {}
        self.current_playlist = None
        self.adding_song = False  # Flag to indicate if we are adding a song
        self.active_listbox = None  # Listbox currently in use

        self.login_frame = tk.Frame(self.master, bg="#121212")
        self.registo_frame = tk.Frame(self.master, bg="#121212")
        self.main_frame = tk.Frame(self.master, bg="#121212")
        self.biblioteca_frame = tk.Frame(self.master, bg="#121212")
        self.nova_playlist_frame = tk.Frame(self.master, bg="#121212")
        self.escolher_playlist_frame = tk.Frame(self.master, bg="#121212")
        self.editar_playlist_frame = tk.Frame(self.master, bg="#121212")
        self.musicas_playlist_frame = tk.Frame(self.master, bg="#121212")
        self.personalizar_playlist_frame = tk.Frame(self.master, bg="#121212")

        self.criar_login_frame()
        self.criar_registo_frame()
        self.criar_main_frame()
        self.criar_biblioteca_frame()
        self.criar_nova_playlist_frame()
        self.criar_escolher_playlist_frame()
        self.criar_editar_playlist_frame()
        self.criar_musicas_playlist_frame()
        self.criar_personalizar_playlist_frame()

        self.show_login_frame()

    def criar_login_frame(self):
        label = tk.Label(self.login_frame, text="Bem vindo ao SpotMuzik!", font=("Calibri", 30, "bold"), bg="#121212", fg="#f3f4ef")
        label.pack(pady=20)

        username_label = tk.Label(self.login_frame, text="Username", font=("Calibri", 16, "bold"), bg="#121212", fg="#f3f4ef")
        username_label.pack(pady=5)

        self.username_entry = ctk.CTkEntry(self.login_frame, width=200, font=("Calibri", 16), placeholder_text="Username")
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self.login_frame, text="Password", font=("Calibri", 16, "bold"), bg="#121212", fg="#f3f4ef")
        password_label.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self.login_frame, width=200, font=("Calibri", 16), show="*", placeholder_text="Password")
        self.password_entry.pack(pady=5)

        login_button = ctk.CTkButton(self.login_frame, text="Iniciar sessão", command=self.login, font=("Calibri", 16), fg_color="#004080")
        login_button.pack(pady=30)

        register_button = ctk.CTkButton(self.login_frame, text="Não tens conta?", command=self.show_registo_frame, font=("Calibri", 16), fg_color="#004080")
        register_button.pack(pady=10)

    def criar_registo_frame(self):
        label = tk.Label(self.registo_frame, text="Registar", font=("Calibri", 30, "bold"), bg="#121212", fg="#f3f4ef")
        label.pack(pady=20)

        username_label = tk.Label(self.registo_frame, text="Username", font=("Calibri", 16, "bold"), bg="#121212", fg="#f3f4ef")
        username_label.pack(pady=5)

        self.registo_username_entry = ctk.CTkEntry(self.registo_frame, width=200, font=("Calibri", 16), placeholder_text="Username")
        self.registo_username_entry.pack(pady=5)

        password_label = tk.Label(self.registo_frame, text="Password", font=("Calibri", 16, "bold"), bg="#121212", fg="#f3f4ef")
        password_label.pack(pady=5)

        self.registo_password_entry = ctk.CTkEntry(self.registo_frame, width=200, font=("Calibri", 16), show="*", placeholder_text="Password")
        self.registo_password_entry.pack(pady=5)

        confirm_password_label = tk.Label(self.registo_frame, text="Confirme a Password", font=("Calibri", 16, "bold"), bg="#121212", fg="#f3f4ef")
        confirm_password_label.pack(pady=5)

        self.segunda_password_entry = ctk.CTkEntry(self.registo_frame, width=200, font=("Calibri", 16), show="*", placeholder_text="Confirme Password")
        self.segunda_password_entry.pack(pady=5)

        register_button = ctk.CTkButton(self.registo_frame, text="Confirmar", command=self.registar, font=("Calibri", 16), fg_color="#004080")
        register_button.pack(pady=25)

        back_to_login_button = ctk.CTkButton(self.registo_frame, text="Login", command=self.show_login_frame, font=("Calibri", 16), fg_color="#004080")
        back_to_login_button.pack(pady=10)

    def criar_main_frame(self):
        # Cria uma label para o título
        titulo = tk.Label(self.main_frame, text="Music Player", font=("Calibri", 30, "bold"), bg="#121212", fg="#f3f4ef")
        titulo.pack(pady=10)

        # Cria um frame para o botão e a barra de busca
        top_frame = tk.Frame(self.main_frame, bg="#121212")
        top_frame.pack(pady=20)

        # Cria um botão para carregar as musicas
        button_carregar_musicas = ctk.CTkButton(top_frame, text="Carregar Musicas", font=("Calibri", 18), fg_color="#004080", command=self.load_top_tracks)
        button_carregar_musicas.pack(side=tk.LEFT, padx=5)

        # Cria um botão para criar as playlist
        button_biblioteca = ctk.CTkButton(top_frame, text="Biblioteca", command=self.show_biblioteca_frame, font=("Calibri", 18), fg_color="#004080")
        button_biblioteca.pack(side=tk.LEFT, padx=5)

        # Cria um botão para remover musicas
        button_remover_musicas = ctk.CTkButton(top_frame, text="Remover Música", command=self.remove_song, font=("Calibri", 18), fg_color="#004080")
        button_remover_musicas.pack(side=tk.LEFT, padx=5)

        # Cria uma Listbox para mostrar as musicas disponiveis
        self.listbox = tk.Listbox(self.main_frame, width=50, font=("Calibri", 16), bg="#181818", fg="#f3f4ef")
        self.listbox.pack(pady=10)
        self.listbox.bind("<Double-Button-1>", self.double_click_main)

        # Cria uma frame para os botões de controlo
        button_frame = tk.Frame(self.main_frame, bg="#121212")
        button_frame.pack(pady=15)

        # Cria um botão para ir para a musica anterior
        button_previous = ctk.CTkButton(button_frame, text="<<", width=50, font=("Calibri", 18), bg_color="#121212", fg_color="#004080", command=self.previous_song)
        button_previous.pack(side=tk.LEFT, padx=5)

        # Cria um botão para tocar a musica
        button_play = ctk.CTkButton(button_frame, text="Play", width=50, font=("Calibri", 18), bg_color="#121212", fg_color="#004080", command=self.play_music)
        button_play.pack(side=tk.LEFT, padx=5)

        # Cria um botão para continuar a musica
        button_continue = ctk.CTkButton(button_frame, text="Continuar", width=50, font=("Calibri", 18), bg_color="#121212", fg_color="#004080", command=self.continue_music)
        button_continue.pack(side=tk.LEFT, padx=5)

        # Cria um botão para pausar a musica
        button_pause = ctk.CTkButton(button_frame, text="Pausar", width=50, font=("Calibri", 18), bg_color="#121212", fg_color="#004080", command=self.pause_music)
        button_pause.pack(side=tk.LEFT, padx=5)

        # Cria um botão para ir para a próxima musica
        button_next = ctk.CTkButton(button_frame, text=">>", width=50, font=("Calibri", 18), bg_color="#121212", fg_color="#004080", command=self.next_song)
        button_next.pack(side=tk.LEFT, padx=5)

        # Cria uma entry para o utilizador pesquisar as musicas
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(button_frame, textvariable=self.search_var, font=("Calibri", 16), width=200)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_var.trace("w", self.filter_songs)

        # Lista para armazenar os paths da musica
        self.songs = []
        self.filtered_songs = []
        self.track_uris = []
        self.playlist_uris = {}

        self.main_frame.pack_forget()

    def criar_biblioteca_frame(self):
        label = tk.Label(self.biblioteca_frame, text="Biblioteca", font=("Calibri", 30, "bold"), bg="#121212", fg="#f3f4ef")
        label.pack(pady=20)

        criar_playlist_button = ctk.CTkButton(self.biblioteca_frame, text="Criar Playlist", command=self.show_nova_playlist_frame, font=("Calibri", 16), fg_color="#004080")
        criar_playlist_button.pack(pady=20)

        escolher_playlist_button = ctk.CTkButton(self.biblioteca_frame, text="Escolher Playlist", command=self.show_escolher_playlist_frame, font=("Calibri", 16), fg_color="#004080")
        escolher_playlist_button.pack(pady=20)

        editar_playlist_button = ctk.CTkButton(self.biblioteca_frame, text="Editar Playlist", command=self.show_editar_playlist_frame, font=("Calibri", 16), fg_color="#004080")
        editar_playlist_button.pack(pady=20)

        voltar_button = ctk.CTkButton(self.biblioteca_frame, text="Voltar", command=self.show_main_frame, font=("Calibri", 16), fg_color="#004080")
        voltar_button.pack(pady=20)

    def criar_nova_playlist_frame(self):
        label = tk.Label(self.nova_playlist_frame, text="Nova Playlist", font=("Calibri", 30, "bold"), bg="#121212", fg="#f3f4ef")
        label.pack(pady=20)

        playlist_name_label = tk.Label(self.nova_playlist_frame, text="Nome da Playlist", font=("Calibri", 16, "bold"), bg="#121212", fg="#f3f4ef")
        playlist_name_label.pack(pady=5)

        self.playlist_name_entry = ctk.CTkEntry(self.nova_playlist_frame, width=200, font=("Calibri", 16), placeholder_text="Nome da Playlist")
        self.playlist_name_entry.pack(pady=5)

        create_button = ctk.CTkButton(self.nova_playlist_frame, text="Criar", command=self.criar_playlist, font=("Calibri", 16), fg_color="#004080")
        create_button.pack(pady=20)

        voltar_biblioteca_button = ctk.CTkButton(self.nova_playlist_frame, text="Voltar", command=self.show_biblioteca_frame, font=("Calibri", 16), fg_color="#004080")
        voltar_biblioteca_button.pack(pady=10)

    def criar_escolher_playlist_frame(self):
        label = tk.Label(self.escolher_playlist_frame, text="Escolher Playlist", font=("Calibri", 30, "bold"), bg="#121212", fg="#f3f4ef")
        label.pack(pady=20)

        self.playlist_listbox = tk.Listbox(self.escolher_playlist_frame, width=30, font=("Calibri", 16), bg="#181818", fg="#f3f4ef")
        self.playlist_listbox.pack(pady=10)
        self.playlist_listbox.bind("<Double-Button-1>", self.double_click_escolher)

        voltar_biblioteca_button = ctk.CTkButton(self.escolher_playlist_frame, text="Voltar", command=self.show_biblioteca_frame, font=("Calibri", 16), fg_color="#004080")
        voltar_biblioteca_button.pack(pady=5)

    def criar_editar_playlist_frame(self):
        label = tk.Label(self.editar_playlist_frame, text="Editar Playlist", font=("Calibri", 30, "bold"), bg="#121212", fg="#f3f4ef")
        label.pack(pady=20)

        self.playlist_editar_listbox = tk.Listbox(self.editar_playlist_frame, width=30, font=("Calibri", 16), bg="#181818", fg="#f3f4ef")
        self.playlist_editar_listbox.pack(pady=10)
        self.playlist_editar_listbox.bind("<Double-Button-1>", self.double_click_editar)

        voltar_biblioteca_button = ctk.CTkButton(self.editar_playlist_frame, text="Voltar", command=self.show_biblioteca_frame, font=("Calibri", 16), fg_color="#004080")
        voltar_biblioteca_button.pack(pady=5)

    def criar_musicas_playlist_frame(self):
        self.playlist_title_label = tk.Label(self.musicas_playlist_frame, text="", font=("Calibri", 30, "bold"), bg="#121212", fg="#f3f4ef")
        self.playlist_title_label.pack(pady=10)

        self.musicas_listbox = tk.Listbox(self.musicas_playlist_frame, width=50, font=("Calibri", 16), bg="#181818", fg="#f3f4ef")
        self.musicas_listbox.pack(pady=10)

        button_frame = tk.Frame(self.musicas_playlist_frame, bg="#121212")
        button_frame.pack(pady=15)

        button_previous = ctk.CTkButton(button_frame, text="<<", width=50, font=("Calibri", 18), bg_color="#121212", fg_color="#004080", command=self.previous_song)
        button_previous.pack(side=tk.LEFT, padx=5)

        button_play = ctk.CTkButton(button_frame, text="Play", width=50, font=("Calibri", 18), bg_color="#121212", fg_color="#004080", command=self.play_music)
        button_play.pack(side=tk.LEFT, padx=5)

        button_continue = ctk.CTkButton(button_frame, text="Continuar", width=50, font=("Calibri", 18), bg_color="#121212", fg_color="#004080", command=self.continue_music)
        button_continue.pack(side=tk.LEFT, padx=5)

        button_pause = ctk.CTkButton(button_frame, text="Pausar", width=50, font=("Calibri", 18), bg_color="#121212", fg_color="#004080", command=self.pause_music)
        button_pause.pack(side=tk.LEFT, padx=5)

        button_next = ctk.CTkButton(button_frame, text=">>", width=50, font=("Calibri", 18), bg_color="#121212", fg_color="#004080", command=self.next_song)
        button_next.pack(side=tk.LEFT, padx=5)

        back_button = ctk.CTkButton(self.musicas_playlist_frame, text="Voltar", command=self.show_biblioteca_frame, font=("Calibri", 16), fg_color="#004080")
        back_button.pack(pady=10)

    def criar_personalizar_playlist_frame(self):
        # Criar frame de personalização de playlist
        self.personalizar_playlist_frame = tk.Frame(self.master, bg="#121212")  

        # Label para o nome da playlist
        self.personalizar_playlist_label = tk.Label(self.personalizar_playlist_frame, text="", font=("Calibri", 30, "bold"), bg="#121212", fg="#f3f4ef")
        self.personalizar_playlist_label.pack(pady=10)

        # Frame para os botões no topo
        top_button_frame = tk.Frame(self.personalizar_playlist_frame, bg="#121212")
        top_button_frame.pack(pady=10)

        # Botão para adicionar música
        self.adicionar_musica_button = ctk.CTkButton(top_button_frame, text="Adicionar Música", width=15, font=("Calibri", 16), fg_color="#004080", command=self.show_main_frame_for_add_song)
        self.adicionar_musica_button.pack(side=tk.LEFT, padx=5)

        # Botão para remover playlist
        self.remover_playlist_button = ctk.CTkButton(top_button_frame, text="Remover Playlist", command=self.remover_playlist, font=("Calibri", 16), fg_color="#004080")
        self.remover_playlist_button.pack(side=tk.LEFT, padx=5)

        # Botão para remover música
        self.remover_musica_button = ctk.CTkButton(top_button_frame, text="Remover Música", width=15, font=("Calibri", 16), fg_color="#004080", command=self.remove_song_from_playlist)
        self.remover_musica_button.pack(side=tk.LEFT, padx=5)

        # Listbox para as músicas da playlist
        self.personalizar_musicas_listbox = tk.Listbox(self.personalizar_playlist_frame, width=50, font=("Calibri", 16), bg="#181818", fg="#f3f4ef")
        self.personalizar_musicas_listbox.pack(pady=10)

        # Frame para o botão de voltar na parte inferior
        bottom_button_frame = tk.Frame(self.personalizar_playlist_frame, bg="#121212")
        bottom_button_frame.pack(pady=15)

        # Botão para voltar
        self.voltar_button = ctk.CTkButton(bottom_button_frame, text="Voltar", width=15, font=("Calibri", 16), fg_color="#004080", command=self.show_editar_playlist_frame)
        self.voltar_button.pack()

    def clear_all_frames(self):
        self.login_frame.pack_forget()
        self.registo_frame.pack_forget()
        self.main_frame.pack_forget()
        self.biblioteca_frame.pack_forget()
        self.nova_playlist_frame.pack_forget()
        self.escolher_playlist_frame.pack_forget()
        self.editar_playlist_frame.pack_forget()
        self.musicas_playlist_frame.pack_forget()
        self.personalizar_playlist_frame.pack_forget()

    def show_login_frame(self):
        self.clear_all_frames()
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def show_registo_frame(self):
        self.clear_all_frames()
        self.registo_frame.pack(fill=tk.BOTH, expand=True)

    def show_main_frame(self):
        self.clear_all_frames()
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.active_listbox = self.listbox

    def show_biblioteca_frame(self):
        self.clear_all_frames()
        self.biblioteca_frame.pack(fill=tk.BOTH, expand=True)

    def show_nova_playlist_frame(self):
        self.clear_all_frames()
        self.nova_playlist_frame.pack(fill=tk.BOTH, expand=True)

    def show_escolher_playlist_frame(self):
        self.update_playlist_listbox()
        self.clear_all_frames()
        self.escolher_playlist_frame.pack(fill=tk.BOTH, expand=True)

    def show_editar_playlist_frame(self):
        self.update_playlist_listbox()
        self.clear_all_frames()
        self.editar_playlist_frame.pack(fill=tk.BOTH, expand=True)

    def show_musicas_playlist_frame(self, playlist_name):
        self.clear_all_frames()
        self.update_musicas_playlist_frame(playlist_name)
        self.musicas_playlist_frame.pack(fill=tk.BOTH, expand=True)
        self.active_listbox = self.musicas_listbox
        self.current_playlist = playlist_name

    def show_personalizar_playlist_frame(self, playlist_name):
        self.current_playlist = playlist_name
        self.clear_all_frames()
        self.update_personalizar_playlist_frame(playlist_name)
        self.personalizar_playlist_frame.pack(fill=tk.BOTH, expand=True)
        self.active_listbox = self.personalizar_musicas_listbox

    def show_main_frame_for_add_song(self):
        self.adding_song = True
        self.show_main_frame()

    def criar_playlist(self):
        playlist_name = self.playlist_name_entry.get()
        if playlist_name:
            if playlist_name not in self.playlists:
                self.playlists[playlist_name] = []
                self.playlist_uris[playlist_name] = []
                messagebox.showinfo("Sucesso", f"Playlist '{playlist_name}' criada com sucesso!")
            else:
                messagebox.showerror("Erro", f"Playlist '{playlist_name}' já existe!")
        else:
            messagebox.showerror("Erro", "Nome da playlist não pode ser vazio!")
        self.show_biblioteca_frame()

    def escolher_playlist(self):
        # Carrega todas as playlists disponíveis
        self.playlist_listbox.delete(0, tk.END)
        for playlist_name in self.playlists:
            self.playlist_listbox.insert(tk.END, playlist_name)
        self.show_escolher_playlist_frame()

    def remover_playlist(self):
        # Obtém o nome da playlist selecionada
        selected_playlist = self.personalizar_playlist_label.cget("text")
        if selected_playlist in self.playlists:
            del self.playlists[selected_playlist]
            del self.playlist_uris[selected_playlist]

        # Voltar ao frame de edição de playlists
        self.show_editar_playlist_frame()

    def update_playlist_listbox(self):
        self.playlist_listbox.delete(0, tk.END)
        self.playlist_editar_listbox.delete(0, tk.END)  # Limpa a Listbox
        for playlist_name in self.playlists.keys():
            self.playlist_listbox.insert(tk.END, playlist_name)
            self.playlist_editar_listbox.insert(tk.END, playlist_name)

    def update_musicas_playlist_frame(self, playlist_name):
        self.playlist_title_label.config(text=playlist_name)
        self.musicas_listbox.delete(0, tk.END)
        for song in self.playlists.get(playlist_name, []):
            self.musicas_listbox.insert(tk.END, song)

    def update_personalizar_playlist_frame(self, playlist_name):
        self.personalizar_playlist_label.config(text=playlist_name)
        self.personalizar_musicas_listbox.delete(0, tk.END)
        for song in self.playlists.get(playlist_name, []):
            self.personalizar_musicas_listbox.insert(tk.END, song)

    def load_utilizador(self):
        for nome, password in self.database.fetch_utilizador():
            self.utilizadores.insert_last(Utilizador(nome, password))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        posicao = self.utilizadores.find_utilizador(username)
        if posicao == -1:
            messagebox.showerror("Erro de Login", "Username não encontrado")
        else:
            utilizador = self.utilizadores.get(posicao)
            if utilizador.get_password() == password:
                self.utilizador_login = utilizador
                messagebox.showinfo("Login", "Login efetuado com sucesso")
                self.show_main_frame()
            else:
                messagebox.showerror("Erro de Login", "Senha incorreta")

    def registar(self):
        username = self.registo_username_entry.get()
        password = self.registo_password_entry.get()
        segunda_password = self.segunda_password_entry.get()

        if password != segunda_password:
            messagebox.showerror("Erro", "As passwords não coincidem")
            return

        if self.database.insert_utilizador(username, password):
            self.utilizadores.insert_last(Utilizador(username, password))
            messagebox.showinfo("Sucesso", "Utilizador registado com sucesso")
        else:
            messagebox.showerror("Erro", "Este nome de utilizador já está em uso")

    def double_click_main(self, event):
        if self.adding_song:
            self.add_song()
        else:
            self.play_music()

    def double_click_escolher(self, event):
        selected_index = self.playlist_listbox.curselection()
        if selected_index:
            selected_playlist = self.playlist_listbox.get(selected_index)
            self.show_musicas_playlist_frame(selected_playlist)

    def double_click_editar(self, event):
        selected_index = self.playlist_editar_listbox.curselection()
        if selected_index:
            selected_playlist = self.playlist_editar_listbox.get(selected_index)
            self.show_personalizar_playlist_frame(selected_playlist)

    # barra de pesquisa do main frame
    def update_listbox(self):  # atualiza a listbox de acordo com a pesquisa
        self.listbox.delete(0, tk.END)
        for song in self.filtered_songs:
            self.listbox.insert(tk.END, song)

    def filter_songs(self, *args):  # procura as musicas
        search_term = self.search_var.get().lower()
        self.filtered_songs = [song for song in self.songs if search_term in song.lower()]
        self.update_listbox()

    def load_top_tracks(self):
        try:
            client_id = '9dced3cc009b4a738ffe7d1109d93ce0'
            client_secret = 'e1727724c6dc486da11ba9c624db709b'
            
            spotify = Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
            
            # Procuramos faixas populares (o ecossistema Spotify continua excelente para metadados)
            results = spotify.search(q='year:2025', type='track', limit=20)
            items = results['tracks']['items']
            
            self.songs = [f"{track['artists'][0]['name']} - {track['name']}" for track in items]
            
            # Como vamos buscar o áudio dinamicamente à Deezer no momento do Play,
            # já não precisamos de guardar URLs vazios do Spotify!
            self.track_uris = ["" for _ in items]

            self.listbox.delete(0, tk.END)
            for song in self.songs:
                self.listbox.insert(tk.END, song)
                
            messagebox.showinfo("Sucesso", "Músicas carregadas com sucesso! Prontas para reproduzir via Deezer Sync.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar músicas: {e}")

    def play_music(self):
        if not self.active_listbox or not self.active_listbox.curselection():
            return
            
        selected_index = self.active_listbox.curselection()[0]
        # Obtém o nome legível da música selecionada (ex: "Bad Bunny - LA mUDANZA")
        song_name = self.active_listbox.get(selected_index)
        
        try:
            # --- TRUQUE DA DEEZER API ---
            # Fazemos um request rápido à API pública da Deezer para encontrar a mesma música
            deezer_url = f"https://api.deezer.com/search?q={requests.utils.quote(song_name)}&limit=1"
            deezer_response = requests.get(deezer_url).json()
            
            song_url = None
            if deezer_response.get('data'):
                # Extraímos o preview_url que a Deezer ainda disponibiliza ativamente!
                song_url = deezer_response['data'][0].get('preview')
            
            if not song_url:
                messagebox.showwarning("Áudio Não Encontrado", f"Não foi possível localizar um stream de áudio para:\n{song_name}")
                return

            # Código original de streaming com Pygame (continua igual, mas agora com áudio garantido)
            response = requests.get(song_url)
            if response.status_code == 200:
                self.audio_file = BytesIO(response.content)
                self.audio_file.seek(0)
                pygame.mixer.music.load(self.audio_file, 'mp3')
                pygame.mixer.music.play()
                self.paused = False
                
        except Exception as e:
            messagebox.showerror("Erro de Reprodução", f"Erro ao tentar tocar esta faixa: {e}")
            
    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True  # Define o estado de pausa como True

    def continue_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False  # Reseta o estado de pausa

    def next_song(self):
        if not self.active_listbox or not self.active_listbox.curselection():
            return
        selected_index = self.active_listbox.curselection()[0]
        next_index = (selected_index + 1) % len(self.active_listbox.get(0, tk.END))
        self.active_listbox.select_clear(0, tk.END)
        self.active_listbox.select_set(next_index)
        self.play_music()

    def previous_song(self):
        if not self.active_listbox or not self.active_listbox.curselection():
            return
        selected_index = self.active_listbox.curselection()[0]
        prev_index = (selected_index - 1) % len(self.active_listbox.get(0, tk.END))
        self.active_listbox.select_clear(0, tk.END)
        self.active_listbox.select_set(prev_index)
        self.play_music()

    def remove_song(self):
        selected_index = self.active_listbox.curselection()
        if selected_index:
            self.active_listbox.delete(selected_index)
            del self.songs[selected_index[0]]
            del self.track_uris[selected_index[0]]
            messagebox.showinfo("Removido", "Música removida com sucesso")
        else:
            messagebox.showerror("Erro", "Nenhuma música selecionada para remover")

    def remove_song_from_playlist(self):
        selected_index = self.personalizar_musicas_listbox.curselection()
        if selected_index:
            self.personalizar_musicas_listbox.delete(selected_index)
            del self.playlists[self.current_playlist][selected_index[0]]
            del self.playlist_uris[self.current_playlist][selected_index[0]]
            messagebox.showinfo("Removido", "Música removida da playlist com sucesso")
        else:
            messagebox.showerror("Erro", "Nenhuma música selecionada para remover")

    def add_song(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            song = self.songs[selected_index[0]]
            song_url = self.track_uris[selected_index[0]]
            if self.current_playlist:
                if song in self.playlists[self.current_playlist]:
                    messagebox.showerror("Erro", "A música já está na playlist.")
                else:
                    self.playlists[self.current_playlist].append(song)
                    self.playlist_uris[self.current_playlist].append(song_url)
                    messagebox.showinfo("Adicionado", f"Música '{song}' adicionada à playlist '{self.current_playlist}'")
                    self.show_personalizar_playlist_frame(self.current_playlist)  # Return to playlist view
            else:
                messagebox.showerror("Erro", "Nenhuma playlist selecionada.")
        else:
            messagebox.showerror("Erro", "Nenhuma música selecionada para adicionar.")
        self.adding_song = False