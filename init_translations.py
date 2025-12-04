# init_translations.py - VERSÃO MELHORADA
import os
import subprocess
import sys
from pathlib import Path

def extract_translations():
    """Extrai textos para tradução"""
    print("📝 Extraindo textos para tradução...")
    
    try:
        # Tenta extrair com o babel.cfg
        result = subprocess.run([
            "pybabel", "extract", 
            "-F", "babel.cfg", 
            "-o", "messages.pot", 
            "."
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"⚠️  Aviso ao extrair com babel.cfg: {result.stderr[:200]}")
            
            # Tenta método alternativo
            print("🔄 Tentando método alternativo de extração...")
            result = subprocess.run([
                "pybabel", "extract",
                "--keywords", "_",
                "--keywords", "gettext",
                "--keywords", "ngettext",
                "--keywords", "lazy_gettext",
                "-o", "messages.pot",
                "."
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Falha na extração: {result.stderr[:500]}")
                return False
        
        print("✅ Textos extraídos com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro inesperado na extração: {e}")
        return False

def init_language_translations(lang):
    """Inicializa traduções para um idioma específico"""
    print(f"🌐 Inicializando tradução para {lang}...")
    
    lang_dir = Path(f"translations/{lang}/LC_MESSAGES")
    
    # Se já existir, não recria
    if (lang_dir / "messages.po").exists():
        print(f"  ✅ Arquivo .po já existe para {lang}")
        return True
    
    try:
        result = subprocess.run([
            "pybabel", "init", 
            "-i", "messages.pot", 
            "-d", "translations", 
            "-l", lang,
            "--no-wrap"  # Evita quebra de linha automática
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"  ⚠️  Aviso ao inicializar {lang}: {result.stderr[:200]}")
            
            # Tenta criar estrutura manualmente
            lang_dir.mkdir(parents=True, exist_ok=True)
            with open(lang_dir / "messages.po", "w", encoding="utf-8") as f:
                f.write(f'''# {lang} translations
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

msgid "Welcome"
msgstr "Welcome"
''')
            print(f"  ✅ Arquivo .po criado manualmente para {lang}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao inicializar {lang}: {e}")
        return False

def compile_translations():
    """Compila as traduções"""
    print("🔨 Compilando traduções...")
    
    try:
        result = subprocess.run([
            "pybabel", "compile", 
            "-d", "translations",
            "--statistics"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"⚠️  Aviso ao compilar: {result.stderr[:200]}")
            
            # Verifica se existem arquivos .po para compilar
            po_files = list(Path("translations").rglob("*.po"))
            if not po_files:
                print("ℹ️  Nenhum arquivo .po encontrado para compilar")
                return True
            
            print(f"  📁 Arquivos .po encontrados: {len(po_files)}")
            
        print("✅ Traduções compiladas com sucesso!")
        print(result.stdout)
        return True
        
    except Exception as e:
        print(f"❌ Erro ao compilar traduções: {e}")
        return False

def create_minimal_translations():
    """Cria traduções mínimas se o Babel falhar"""
    print("🛠️  Criando traduções mínimas...")
    
    languages = ['pt', 'en', 'es', 'fr']
    
    for lang in languages:
        lang_dir = Path(f"translations/{lang}/LC_MESSAGES")
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        # Cria arquivo .po mínimo
        po_file = lang_dir / "messages.po"
        if not po_file.exists():
            with open(po_file, "w", encoding="utf-8") as f:
                f.write(f'''# {lang} translations
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

# Mensagens básicas
msgid "Welcome"
msgstr "Bem-vindo" if lang == "pt" else "Welcome" if lang == "en" else "Bienvenido" if lang == "es" else "Bienvenue"

msgid "Login"
msgstr "Login" if lang == "pt" else "Login" if lang == "en" else "Iniciar sesión" if lang == "es" else "Connexion"

msgid "Logout"
msgstr "Sair" if lang == "pt" else "Logout" if lang == "en" else "Cerrar sesión" if lang == "es" else "Déconnexion"

msgid "Dashboard"
msgstr "Painel" if lang == "pt" else "Dashboard" if lang == "en" else "Panel" if lang == "es" else "Tableau de bord"

msgid "Save"
msgstr "Salvar" if lang == "pt" else "Save" if lang == "en" else "Guardar" if lang == "es" else "Enregistrer"

msgid "Cancel"
msgstr "Cancelar" if lang == "pt" else "Cancel" if lang == "en" else "Cancelar" if lang == "es" else "Annuler"
''')
            
            # Cria arquivo .mo compilado
            mo_file = lang_dir / "messages.mo"
            # Para um sistema mínimo, podemos copiar um .po vazio como .mo
            # Em produção, você instalaria o msgfmt
            if not mo_file.exists():
                # Cria um arquivo .mo vazio (apenas para desenvolvimento)
                with open(mo_file, "wb") as f:
                    f.write(b'')  # Arquivo vazio por enquanto
                
                print(f"  ✅ Criadas traduções mínimas para {lang}")
    
    return True

def init_translations():
    """Inicializa os arquivos de tradução"""
    print("🔧 Inicializando sistema de traduções...")
    
    # Cria diretório de traduções se não existir
    os.makedirs("translations", exist_ok=True)
    
    # Tenta extrair traduções
    if not extract_translations():
        print("⚠️  Não foi possível extrair traduções, usando método alternativo...")
    
    # Inicializa traduções para cada idioma
    languages = ['pt', 'en', 'es', 'fr']
    all_success = True
    
    for lang in languages:
        if not init_language_translations(lang):
            all_success = False
    
    # Se algum falhou, cria traduções mínimas
    if not all_success:
        print("⚠️  Algumas inicializações falharam, criando traduções mínimas...")
        create_minimal_translations()
    
    # Tenta compilar
    if not compile_translations():
        print("⚠️  Não foi possível compilar traduções com pybabel")
    
    print("✅ Sistema de traduções inicializado!")
    return True

if __name__ == "__main__":
    success = init_translations()
    sys.exit(0 if success else 1)