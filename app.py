import os
import subprocess
import shutil
import tempfile
import json
from tkinter import filedialog, messagebox
import customtkinter as ctk #type: ignore 
ctk.deactivate_automatic_dpi_awareness()


# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DebPackageBuilder(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração da janela principal
        self.title("Deb Package Builder - v2.0")
        self.geometry("1000x800")
        self.minsize(900, 700)
        
        # Variáveis para armazenar dados
        self.package_info = {}
        self.binary_files = []
        self.extra_files = []
        self.temp_dir = None
        self.output_dir = os.path.expanduser("~/deb-packages")
        
        # Criar diretório de saída se não existir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Configurar layout
        self.setup_ui()
        
    def setup_ui(self):
        """Configura todos os elementos da interface"""
        
        # Frame principal com scroll
        self.main_frame = ctk.CTkScrollableFrame(self, label_text="Criador de Pacotes .deb")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Seção: Informações do Pacote
        self.create_package_info_section()
        
        # Seção: Integração com o Sistema
        self.create_integration_section()
        
        # Seção: Arquivos
        self.create_files_section()
        
        # Seção: Opções Avançadas
        self.create_advanced_options()
        
        # Seção: Ações
        self.create_actions_section()
        
        # Status bar
        self.status_label = ctk.CTkLabel(self, text="Pronto", font=("Arial", 12))
        self.status_label.pack(pady=(0, 10))
        
    def create_package_info_section(self):
        """Cria a seção de informações do pacote"""
        info_frame = ctk.CTkFrame(self.main_frame)
        info_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(info_frame, text="Informações do Pacote", font=("Arial", 16, "bold")).pack(pady=5)
        
        # Grid para campos
        grid_frame = ctk.CTkFrame(info_frame)
        grid_frame.pack(fill="x", padx=20, pady=10)
        
        # Nome do pacote
        ctk.CTkLabel(grid_frame, text="Nome do Pacote:*").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.package_name = ctk.CTkEntry(grid_frame, placeholder_text="Ex: meu-app", width=300)
        self.package_name.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Nome do executável (diferente do nome do pacote)
        ctk.CTkLabel(grid_frame, text="Nome do Executável:*").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.executable_name = ctk.CTkEntry(grid_frame, placeholder_text="Ex: meu-app", width=200)
        self.executable_name.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Versão
        ctk.CTkLabel(grid_frame, text="Versão:*").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.package_version = ctk.CTkEntry(grid_frame, placeholder_text="Ex: 1.0.0", width=200)
        self.package_version.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Arquitetura
        ctk.CTkLabel(grid_frame, text="Arquitetura:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.architecture = ctk.CTkComboBox(grid_frame, values=["amd64", "i386", "arm64", "armhf", "all"], width=150)
        self.architecture.set("amd64")
        self.architecture.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Mantenedor
        ctk.CTkLabel(grid_frame, text="Mantenedor:*").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.maintainer = ctk.CTkEntry(grid_frame, placeholder_text="Nome <email@exemplo.com>", width=400)
        self.maintainer.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Descrição
        ctk.CTkLabel(grid_frame, text="Descrição:*").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.description = ctk.CTkEntry(grid_frame, placeholder_text="Descrição curta do pacote", width=400)
        self.description.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Descrição longa
        ctk.CTkLabel(grid_frame, text="Descrição Longa:").grid(row=5, column=0, padx=5, pady=5, sticky="nw")
        self.long_description = ctk.CTkTextbox(grid_frame, height=60, width=400)
        self.long_description.grid(row=5, column=1, columnspan=2, padx=5, pady=5)
        
    def create_integration_section(self):
        """Cria a seção de integração com o sistema"""
        integration_frame = ctk.CTkFrame(self.main_frame)
        integration_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(integration_frame, text="Integração com o Sistema", font=("Arial", 16, "bold")).pack(pady=5)
        
        grid_frame = ctk.CTkFrame(integration_frame)
        grid_frame.pack(fill="x", padx=20, pady=10)
        
        # Nome para o menu
        ctk.CTkLabel(grid_frame, text="Nome no Menu:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.menu_name = ctk.CTkEntry(grid_frame, placeholder_text="Meu Aplicativo", width=300)
        self.menu_name.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Categoria do aplicativo
        ctk.CTkLabel(grid_frame, text="Categoria:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.app_category = ctk.CTkComboBox(grid_frame, values=[
            "Development", "Education", "Game", "Graphics", "Network", 
            "Office", "Science", "Settings", "System", "Utility", "AudioVideo"
        ], width=200)
        self.app_category.set("Utility")
        self.app_category.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Ícone
        ctk.CTkLabel(grid_frame, text="Ícone do Aplicativo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.icon_path = ctk.CTkEntry(grid_frame, placeholder_text="Caminho para o ícone (.png/.svg)", width=350)
        self.icon_path.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        self.icon_btn = ctk.CTkButton(grid_frame, text="Selecionar Ícone", command=self.select_icon, width=120)
        self.icon_btn.grid(row=2, column=2, padx=5, pady=5)
        
    def create_files_section(self):
        """Cria a seção de seleção de arquivos"""
        files_frame = ctk.CTkFrame(self.main_frame)
        files_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(files_frame, text="Arquivos Binários e Recursos", font=("Arial", 16, "bold")).pack(pady=5)
        
        # Frame para botões de arquivos
        btn_frame = ctk.CTkFrame(files_frame)
        btn_frame.pack(fill="x", padx=20, pady=5)
        
        self.add_files_btn = ctk.CTkButton(btn_frame, text="Adicionar Arquivos", command=self.add_files)
        self.add_files_btn.pack(side="left", padx=5)
        
        self.add_folder_btn = ctk.CTkButton(btn_frame, text="Adicionar Pasta", command=self.add_folder)
        self.add_folder_btn.pack(side="left", padx=5)
        
        self.add_extra_files_btn = ctk.CTkButton(btn_frame, text="Adicionar Recursos (ícones, etc)", command=self.add_extra_files)
        self.add_extra_files_btn.pack(side="left", padx=5)
        
        self.clear_files_btn = ctk.CTkButton(btn_frame, text="Limpar Lista", command=self.clear_files, fg_color="red")
        self.clear_files_btn.pack(side="left", padx=5)
        
        # Lista de arquivos
        self.files_listbox = ctk.CTkTextbox(files_frame, height=150)
        self.files_listbox.pack(fill="x", padx=20, pady=10)
        self.files_listbox.configure(state="disabled")
        
    def create_advanced_options(self):
        """Cria a seção de opções avançadas"""
        adv_frame = ctk.CTkFrame(self.main_frame)
        adv_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(adv_frame, text="Opções Avançadas", font=("Arial", 16, "bold")).pack(pady=5)
        
        grid_frame = ctk.CTkFrame(adv_frame)
        grid_frame.pack(fill="x", padx=20, pady=10)
        
        # Dependências
        ctk.CTkLabel(grid_frame, text="Dependências:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.dependencies = ctk.CTkEntry(grid_frame, placeholder_text="libc6, libssl1.1 (separado por vírgula)", width=400)
        self.dependencies.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Prioridade
        ctk.CTkLabel(grid_frame, text="Prioridade:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.priority = ctk.CTkComboBox(grid_frame, values=["optional", "required", "important", "standard", "extra"])
        self.priority.set("optional")
        self.priority.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Seção
        ctk.CTkLabel(grid_frame, text="Seção:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.section = ctk.CTkComboBox(grid_frame, values=["utils", "admin", "net", "web", "libs", "devel", "doc"])
        self.section.set("utils")
        self.section.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Diretório de instalação
        ctk.CTkLabel(grid_frame, text="Diretório de instalação:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.install_dir = ctk.CTkEntry(grid_frame, placeholder_text="/usr/local/bin (padrão)", width=400)
        self.install_dir.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Scripts
        ctk.CTkLabel(grid_frame, text="Script pós-instalação:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.postinst_script = ctk.CTkEntry(grid_frame, placeholder_text="Caminho para script postinst", width=300)
        self.postinst_script.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        self.postinst_btn = ctk.CTkButton(grid_frame, text="Selecionar", command=self.select_postinst, width=100)
        self.postinst_btn.grid(row=4, column=2, padx=5, pady=5)
        
        ctk.CTkLabel(grid_frame, text="Script pré-remoção:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.prerm_script = ctk.CTkEntry(grid_frame, placeholder_text="Caminho para script prerm", width=300)
        self.prerm_script.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        self.prerm_btn = ctk.CTkButton(grid_frame, text="Selecionar", command=self.select_prerm, width=100)
        self.prerm_btn.grid(row=5, column=2, padx=5, pady=5)
        
    def create_actions_section(self):
        """Cria a seção de ações"""
        actions_frame = ctk.CTkFrame(self.main_frame)
        actions_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(actions_frame, text="Ações", font=("Arial", 16, "bold")).pack(pady=5)
        
        btn_frame = ctk.CTkFrame(actions_frame)
        btn_frame.pack(pady=10)
        
        self.build_btn = ctk.CTkButton(btn_frame, text="Construir Pacote .deb", command=self.build_package, 
                                       width=200, height=40, font=("Arial", 14, "bold"))
        self.build_btn.pack(side="left", padx=10)
        
        self.save_config_btn = ctk.CTkButton(btn_frame, text="Salvar Configuração", command=self.save_config, 
                                            width=150, fg_color="green")
        self.save_config_btn.pack(side="left", padx=10)
        
        self.load_config_btn = ctk.CTkButton(btn_frame, text="Carregar Configuração", command=self.load_config, 
                                            width=150, fg_color="orange")
        self.load_config_btn.pack(side="left", padx=10)
        
    def add_files(self):
        """Adiciona arquivos à lista"""
        files = filedialog.askopenfilenames(
            title="Selecionar arquivos binários",
            filetypes=[("Arquivos executáveis", "*.bin *.exe *.sh"), ("Todos os arquivos", "*.*")]
        )
        if files:
            for file in files:
                if file not in self.binary_files:
                    self.binary_files.append(file)
            self.update_files_list()
            self.status_label.configure(text=f"Adicionados {len(files)} arquivos")
    
    def add_extra_files(self):
        """Adiciona arquivos extras (ícones, documentação, etc)"""
        files = filedialog.askopenfilenames(
            title="Selecionar arquivos de recursos",
            filetypes=[("Todos os arquivos", "*.*")]
        )
        if files:
            for file in files:
                if file not in self.extra_files:
                    self.extra_files.append(file)
            self.update_files_list()
            self.status_label.configure(text=f"Adicionados {len(files)} arquivos de recursos")
    
    def add_folder(self):
        """Adiciona uma pasta inteira"""
        folder = filedialog.askdirectory(title="Selecionar pasta com arquivos")
        if folder:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path not in self.binary_files:
                        self.binary_files.append(file_path)
            self.update_files_list()
            self.status_label.configure(text=f"Adicionados arquivos da pasta: {folder}")
    
    def clear_files(self):
        """Limpa a lista de arquivos"""
        self.binary_files = []
        self.extra_files = []
        self.update_files_list()
        self.status_label.configure(text="Lista de arquivos limpa")
    
    def update_files_list(self):
        """Atualiza a listbox com os arquivos selecionados"""
        self.files_listbox.configure(state="normal")
        self.files_listbox.delete("1.0", "end")
        
        if not self.binary_files and not self.extra_files:
            self.files_listbox.insert("1.0", "Nenhum arquivo selecionado")
        else:
            if self.binary_files:
                self.files_listbox.insert("end", "=== ARQUIVOS BINÁRIOS ===\n")
                for i, file in enumerate(self.binary_files, 1):
                    self.files_listbox.insert("end", f"{i}. {file}\n")
            
            if self.extra_files:
                self.files_listbox.insert("end", "\n=== ARQUIVOS DE RECURSOS ===\n")
                for i, file in enumerate(self.extra_files, 1):
                    self.files_listbox.insert("end", f"{i}. {file}\n")
        
        self.files_listbox.configure(state="disabled")
    
    def select_icon(self):
        """Seleciona ícone para o aplicativo"""
        file = filedialog.askopenfilename(
            title="Selecionar ícone do aplicativo",
            filetypes=[("Imagens", "*.png *.svg *.jpg *.jpeg *.xpm"), ("Todos os arquivos", "*.*")]
        )
        if file:
            self.icon_path.delete(0, "end")
            self.icon_path.insert(0, file)
    
    def select_postinst(self):
        """Seleciona script de pós-instalação"""
        file = filedialog.askopenfilename(title="Selecionar script postinst")
        if file:
            self.postinst_script.delete(0, "end")
            self.postinst_script.insert(0, file)
    
    def select_prerm(self):
        """Seleciona script de pré-remoção"""
        file = filedialog.askopenfilename(title="Selecionar script prerm")
        if file:
            self.prerm_script.delete(0, "end")
            self.prerm_script.insert(0, file)
    
    def validate_inputs(self):
        """Valida os campos obrigatórios"""
        if not self.package_name.get():
            messagebox.showerror("Erro", "Nome do pacote é obrigatório")
            return False
        
        if not self.executable_name.get() and not self.binary_files:
            messagebox.showerror("Erro", "Nome do executável ou arquivo binário é obrigatório")
            return False
        
        if not self.package_version.get():
            messagebox.showerror("Erro", "Versão do pacote é obrigatória")
            return False
        
        if not self.maintainer.get():
            messagebox.showerror("Erro", "Mantenedor é obrigatório")
            return False
        
        if not self.description.get():
            messagebox.showerror("Erro", "Descrição é obrigatória")
            return False
        
        if not self.binary_files:
            messagebox.showerror("Erro", "Selecione pelo menos um arquivo binário")
            return False
        
        # Se não tiver nome do executável, usar o nome do primeiro arquivo
        if not self.executable_name.get():
            self.executable_name.insert(0, os.path.basename(self.binary_files[0]))
        
        return True
    
    def create_desktop_file(self, deb_dir):
        """Cria arquivo .desktop para integração com o menu"""
        exec_name = self.executable_name.get()
        app_name = self.menu_name.get() or self.package_name.get()
        
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={app_name}
Comment={self.description.get()}
Exec={exec_name}
Icon={exec_name}
Terminal=false
Categories={self.app_category.get()};
"""
        
        desktop_dir = os.path.join(deb_dir, "usr", "share", "applications")
        os.makedirs(desktop_dir, exist_ok=True)
        
        desktop_file = os.path.join(desktop_dir, f"{self.package_name.get()}.desktop")
        with open(desktop_file, "w") as f:
            f.write(desktop_content)
        
        os.chmod(desktop_file, 0o644)
        return desktop_file
    
    def install_icon(self, deb_dir):
        """Instala o ícone do aplicativo"""
        if self.icon_path.get() and os.path.exists(self.icon_path.get()):
            icon_dir = os.path.join(deb_dir, "usr", "share", "icons", "hicolor")
            
            # Determinar tamanho do ícone
            icon_ext = os.path.splitext(self.icon_path.get())[1].lower()
            if icon_ext in ['.svg']:
                size_dir = "scalable"
            elif icon_ext in ['.png', '.jpg', '.jpeg', '.xpm']:
                size_dir = "256x256"
            else:
                size_dir = "256x256"
            
            icon_path = os.path.join(icon_dir, size_dir, "apps")
            os.makedirs(icon_path, exist_ok=True)
            
            icon_name = f"{self.package_name.get()}{icon_ext}"
            dest_icon = os.path.join(icon_path, icon_name)
            shutil.copy2(self.icon_path.get(), dest_icon)
            os.chmod(dest_icon, 0o644)
            
            return dest_icon
        return None
    
    def create_control_file(self, control_dir):
        """Cria o arquivo de controle do pacote"""
        control_content = f"""Package: {self.package_name.get()}
Version: {self.package_version.get()}
Architecture: {self.architecture.get()}
Maintainer: {self.maintainer.get()}
Description: {self.description.get()}
"""
        
        # Adicionar campos opcionais
        if self.long_description.get("1.0", "end-1c").strip():
            long_desc = self.long_description.get("1.0", "end-1c").strip()
            control_content += f" {long_desc}\n"
        
        if self.dependencies.get():
            control_content += f"Depends: {self.dependencies.get()}\n"
        
        if self.priority.get():
            control_content += f"Priority: {self.priority.get()}\n"
        
        if self.section.get():
            control_content += f"Section: {self.section.get()}\n"
        
        # Escrever arquivo de controle
        control_file = os.path.join(control_dir, "control")
        with open(control_file, "w") as f:
            f.write(control_content)
    
    def create_symlinks(self, deb_dir, install_dir):
        """Cria links simbólicos para o executável nos diretórios padrão"""
        exec_name = self.executable_name.get()
        bin_dir = os.path.join(deb_dir, "usr", "bin")
        os.makedirs(bin_dir, exist_ok=True)
        
        # Criar link simbólico para /usr/bin
        src_file = os.path.join(install_dir, os.path.basename(self.binary_files[0]))
        dst_link = os.path.join(bin_dir, exec_name)
        
        if os.path.exists(src_file):
            # Criar link simbólico relativo
            if os.path.exists(dst_link):
                os.remove(dst_link)
            os.symlink(src_file, dst_link)
            
            # Adicionar aos arquivos de instalação
            return dst_link
        return None
    
    def build_package(self):
        """Constrói o pacote .deb"""
        if not self.validate_inputs():
            return
        
        # Criar diretório temporário
        self.temp_dir = tempfile.mkdtemp()
        self.status_label.configure(text="Preparando construção do pacote...")
        self.build_btn.configure(state="disabled")
        
        try:
            # Criar estrutura de diretórios
            deb_dir = os.path.join(self.temp_dir, "deb")
            control_dir = os.path.join(deb_dir, "DEBIAN")
            
            # Determinar diretório de instalação
            install_path = self.install_dir.get().lstrip("/") or "usr/local/bin"
            install_dir = os.path.join(deb_dir, install_path)
            
            os.makedirs(control_dir, exist_ok=True)
            os.makedirs(install_dir, exist_ok=True)
            
            # Copiar arquivos binários
            self.status_label.configure(text="Copiando arquivos binários...")
            for file_path in self.binary_files:
                if os.path.isfile(file_path):
                    dest_file = os.path.join(install_dir, os.path.basename(file_path))
                    shutil.copy2(file_path, dest_file)
                    # Tornar executável
                    os.chmod(dest_file, 0o755)
            
            # Copiar arquivos extras (recursos)
            self.status_label.configure(text="Copiando recursos...")
            for file_path in self.extra_files:
                if os.path.isfile(file_path):
                    # Determinar diretório de destino baseado no tipo de arquivo
                    dest_dir = self.determine_dest_dir(deb_dir, file_path)
                    if dest_dir:
                        os.makedirs(dest_dir, exist_ok=True)
                        dest_file = os.path.join(dest_dir, os.path.basename(file_path))
                        shutil.copy2(file_path, dest_file)
            
            # Criar arquivo .desktop
            self.status_label.configure(text="Criando integração com o menu...")
            self.create_desktop_file(deb_dir)
            
            # Instalar ícone
            if self.icon_path.get():
                self.status_label.configure(text="Instalando ícone...")
                self.install_icon(deb_dir)
            
            # Criar links simbólicos
            self.status_label.configure(text="Criando links simbólicos...")
            self.create_symlinks(deb_dir, install_dir)
            
            # Criar arquivo de controle
            self.status_label.configure(text="Criando arquivo de controle...")
            self.create_control_file(control_dir)
            
            # Copiar scripts se existirem
            if self.postinst_script.get() and os.path.exists(self.postinst_script.get()):
                shutil.copy2(self.postinst_script.get(), os.path.join(control_dir, "postinst"))
                os.chmod(os.path.join(control_dir, "postinst"), 0o755)
            
            if self.prerm_script.get() and os.path.exists(self.prerm_script.get()):
                shutil.copy2(self.prerm_script.get(), os.path.join(control_dir, "prerm"))
                os.chmod(os.path.join(control_dir, "prerm"), 0o755)
            
            # Construir pacote .deb
            self.status_label.configure(text="Construindo pacote .deb...")
            package_name = f"{self.package_name.get()}_{self.package_version.get()}_{self.architecture.get()}.deb"
            output_path = os.path.join(self.output_dir, package_name)
            
            # Usar dpkg-deb para construir
            cmd = ["dpkg-deb", "--build", deb_dir, output_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.status_label.configure(text=f"Pacote criado com sucesso: {package_name}")
                messagebox.showinfo("Sucesso", 
                    f"Pacote criado com sucesso!\n\n"
                    f"Local: {output_path}\n\n"
                    f"Para instalar: sudo dpkg -i {output_path}\n\n"
                    f"O pacote aparecerá no menu após instalação.")
                self.open_output_folder()
            else:
                error_msg = result.stderr or "Erro desconhecido"
                self.status_label.configure(text="Erro na construção do pacote")
                messagebox.showerror("Erro", f"Falha ao construir pacote:\n{error_msg}")
                
        except Exception as e:
            self.status_label.configure(text="Erro na construção")
            messagebox.showerror("Erro", f"Erro durante a construção:\n{str(e)}")
        
        finally:
            # Limpar arquivos temporários
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            
            self.build_btn.configure(state="normal")
    
    def determine_dest_dir(self, deb_dir, file_path):
        """Determina o diretório de destino para arquivos extras"""
        ext = os.path.splitext(file_path)[1].lower()
        file_name = os.path.basename(file_path).lower()
        
        # Ícones
        if ext in ['.png', '.svg', '.jpg', '.jpeg', '.xpm'] and ('icon' in file_name or 'logo' in file_name):
            return os.path.join(deb_dir, "usr", "share", "icons", "hicolor", "256x256", "apps")
        
        # Documentação
        if ext in ['.pdf', '.txt', '.html'] and ('doc' in file_path or 'manual' in file_path):
            doc_dir = os.path.join(deb_dir, "usr", "share", "doc", self.package_name.get())
            return doc_dir
        
        # Configuração
        if ext in ['.conf', '.cfg', '.ini']:
            return os.path.join(deb_dir, "etc", self.package_name.get())
        
        # Libs
        if ext in ['.so', '.a', '.la']:
            return os.path.join(deb_dir, "usr", "lib", self.package_name.get())
        
        # Outros arquivos vão para o diretório share
        return os.path.join(deb_dir, "usr", "share", self.package_name.get())
    
    def save_config(self):
        """Salva a configuração atual"""
        config = {
            "package_name": self.package_name.get(),
            "executable_name": self.executable_name.get(),
            "package_version": self.package_version.get(),
            "architecture": self.architecture.get(),
            "maintainer": self.maintainer.get(),
            "description": self.description.get(),
            "long_description": self.long_description.get("1.0", "end-1c"),
            "menu_name": self.menu_name.get(),
            "app_category": self.app_category.get(),
            "icon_path": self.icon_path.get(),
            "dependencies": self.dependencies.get(),
            "priority": self.priority.get(),
            "section": self.section.get(),
            "install_dir": self.install_dir.get(),
            "binary_files": self.binary_files,
            "extra_files": self.extra_files,
            "postinst_script": self.postinst_script.get(),
            "prerm_script": self.prerm_script.get()
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Salvar configuração"
        )
        
        if file_path:
            try:
                with open(file_path, "w") as f:
                    json.dump(config, f, indent=2)
                self.status_label.configure(text=f"Configuração salva em: {file_path}")
                messagebox.showinfo("Sucesso", "Configuração salva com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar configuração:\n{str(e)}")
    
    def load_config(self):
        """Carrega uma configuração salva"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Carregar configuração"
        )
        
        if file_path:
            try:
                with open(file_path, "r") as f:
                    config = json.load(f)
                
                # Preencher campos
                self.package_name.delete(0, "end")
                self.package_name.insert(0, config.get("package_name", ""))
                
                self.executable_name.delete(0, "end")
                self.executable_name.insert(0, config.get("executable_name", ""))
                
                self.package_version.delete(0, "end")
                self.package_version.insert(0, config.get("package_version", ""))
                
                self.architecture.set(config.get("architecture", "amd64"))
                
                self.maintainer.delete(0, "end")
                self.maintainer.insert(0, config.get("maintainer", ""))
                
                self.description.delete(0, "end")
                self.description.insert(0, config.get("description", ""))
                
                self.long_description.delete("1.0", "end")
                self.long_description.insert("1.0", config.get("long_description", ""))
                
                self.menu_name.delete(0, "end")
                self.menu_name.insert(0, config.get("menu_name", ""))
                
                self.app_category.set(config.get("app_category", "Utility"))
                
                self.icon_path.delete(0, "end")
                self.icon_path.insert(0, config.get("icon_path", ""))
                
                self.dependencies.delete(0, "end")
                self.dependencies.insert(0, config.get("dependencies", ""))
                
                self.priority.set(config.get("priority", "optional"))
                self.section.set(config.get("section", "utils"))
                
                self.install_dir.delete(0, "end")
                self.install_dir.insert(0, config.get("install_dir", ""))
                
                self.binary_files = config.get("binary_files", [])
                self.extra_files = config.get("extra_files", [])
                self.update_files_list()
                
                self.postinst_script.delete(0, "end")
                self.postinst_script.insert(0, config.get("postinst_script", ""))
                
                self.prerm_script.delete(0, "end")
                self.prerm_script.insert(0, config.get("prerm_script", ""))
                
                self.status_label.configure(text=f"Configuração carregada de: {file_path}")
                messagebox.showinfo("Sucesso", "Configuração carregada com sucesso!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar configuração:\n{str(e)}")
    
    def open_output_folder(self):
        """Abre a pasta de saída"""
        if os.name == 'nt':  # Windows
            os.startfile(self.output_dir)
        else:  # Linux/Mac
            subprocess.run(["xdg-open", self.output_dir])

if __name__ == "__main__":
    # Verificar se dpkg-deb está instalado
    try:
        subprocess.run(["dpkg-deb", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("dpkg-deb não encontrado. Por favor, instale o pacote 'dpkg'")
        print("   Ubuntu/Debian: sudo apt-get install dpkg")
        print("   Red Hat/Fedora: sudo dnf install dpkg")
        
    # Verificar se o sistema é Linux
    if os.name == 'posix':
        try:
            # Verificar se é um sistema Linux
            if not os.path.exists("/usr/share/applications"):
                print(" Este sistema pode não ter a estrutura padrão do Linux.")
        except:
            pass
        
    app = DebPackageBuilder()
    app.mainloop()