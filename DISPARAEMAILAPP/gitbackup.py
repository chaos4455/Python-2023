#este arquivo faz um backup da pasta raiz do projeto


import shutil
import os
import re

def increment_backup_folder(base_folder, project_name):
    # Encontrar backups existentes
    backup_folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
    
    # Filtrar backups relacionados ao projeto específico
    project_backups = [f for f in backup_folders if re.match(fr"{re.escape(project_name)}v\d+", f)]
    
    # Determinar o número do próximo backup
    if project_backups:
        last_backup = max(int(re.search(r"\d+", f).group()) for f in project_backups)
        next_backup_number = last_backup + 1
    else:
        next_backup_number = 1
    
    # Nome do novo backup
    new_backup_folder = f"{project_name}v{next_backup_number:04d}"
    
    return new_backup_folder

def main():
    # Nome do projeto
    project_name = "meuprojeto"
    
    # Diretório base onde o script está localizado
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Diretório de backup
    backup_dir = os.path.join(base_dir, "projeto_backup")
    
    # Garantir que o diretório de backup exista
    os.makedirs(backup_dir, exist_ok=True)
    
    # Nome do novo backup
    new_backup_folder = increment_backup_folder(backup_dir, project_name)
    
    # Caminho completo para o novo backup
    new_backup_path = os.path.join(backup_dir, new_backup_folder)
    
    # Copiar o projeto para o novo backup
    shutil.copytree(base_dir, new_backup_path, ignore=shutil.ignore_patterns('.git', 'projeto_backup'))

    print(f"Backup concluído. Novo backup em: {new_backup_path}")

if __name__ == "__main__":
    main()
