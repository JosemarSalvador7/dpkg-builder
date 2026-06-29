# 📦 Deb Package Builder

<p align="center">
Ferramenta gráfica para criação de pacotes <strong>.deb</strong> de forma simples, rápida e organizada.
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python">
<img src="https://img.shields.io/badge/UI-CustomTkinter-1F6AA5">
<img src="https://img.shields.io/badge/Linux-Debian-E95420">
<img src="https://img.shields.io/badge/License-GPL-blue">
</p>

---

## Visão Geral

O **Deb Package Builder** é uma aplicação desktop desenvolvida em **Python + CustomTkinter** para automatizar a criação de pacotes **Debian (.deb)** através de uma interface gráfica moderna.

A aplicação abstrai a complexidade do empacotamento Debian e permite configurar pacotes completos sem necessidade de editar manualmente ficheiros `control`, `.desktop` ou estruturas internas do sistema.

---

## Funcionalidades

### Construção de Pacotes

* Geração automática de pacotes `.deb`
* Criação da estrutura Debian (`DEBIAN/`)
* Suporte para aplicações e executáveis
* Configuração do diretório de instalação

### Integração com Linux

* Geração automática de ficheiros `.desktop`
* Integração com menu de aplicações
* Instalação automática de ícones
* Criação de links simbólicos em `/usr/bin`

### Configuração Avançada

* Dependências do pacote
* Arquiteturas suportadas:

  * amd64
  * i386
  * arm64
  * armhf
  * all
* Prioridade e secção Debian
* Scripts personalizados:

  * `postinst`
  * `prerm`

### Gestão de Projeto

* Guardar configuração em JSON
* Carregar configurações existentes
* Reutilização de templates de empacotamento

---

## Tecnologias

| Tecnologia    | Finalidade             |
| ------------- | ---------------------- |
| Python        | Lógica da aplicação    |
| CustomTkinter | Interface gráfica      |
| dpkg-deb      | Construção dos pacotes |
| JSON          | Persistência           |
| subprocess    | Execução do sistema    |
| shutil        | Gestão de ficheiros    |

---

## Requisitos

### Sistema Operacional

| Sistema | Compatibilidade |
| ------- | --------------- |
| Linux   | Completa        |
| Windows | Desenvolvimento |
| macOS   | Desenvolvimento |

> A construção final de pacotes `.deb` requer ambiente Linux com `dpkg-deb`.

---

## Instalação

### Clonar repositório

```bash
git clone https://github.com/seu-utilizador/deb-package-builder.git

cd deb-package-builder
```

### Criar ambiente virtual

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

---

## Instalar Dependências

```bash
pip install customtkinter
```

Instalar utilitário Debian:

Ubuntu / Debian:

```bash
sudo apt install dpkg
```

Fedora:

```bash
sudo dnf install dpkg
```

Arch Linux:

```bash
sudo pacman -S dpkg
```

---

## Executar

```bash
python main.py
```

---

## Fluxo de Utilização

```text
Selecionar Aplicação
       ↓
Configurar Metadados
       ↓
Adicionar Recursos
       ↓
Configurar Integração Linux
       ↓
Construir Pacote .deb
```

---

## Estrutura Gerada

```text
meu-pacote/
├── DEBIAN/
│   ├── control
│   ├── postinst
│   └── prerm
│
├── usr/
│   ├── bin/
│   ├── share/
│   │   ├── applications/
│   │   └── icons/
```

---

## Licença

Este projeto está licenciado sob a **GNU General Public License (GPL)**.

Pode utilizar, modificar e redistribuir este software de acordo com os termos da licença.

---

## Autor

**João Salvador Paulo**
Desenvolvedor de Software • Python • Linux • Open Source
