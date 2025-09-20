import os
import subprocess
import shutil
from colorama import Fore, Style
from datetime import datetime

def execute():
    """Fazer backup dos drivers do sistema"""
    try:
        print("Fazendo backup dos drivers...")
        
        # Criar diretório de backup
        backup_dir = os.path.join(os.getcwd(), "driver_backup")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Data para nome do arquivo
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"drivers_backup_{date_str}.zip")
        
        # Comando para exportar drivers usando DISM
        export_command = f'dism /online /export-driver /destination:"{backup_dir}"'
        
        result = subprocess.run(export_command, shell=True, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # Compactar a pasta de drivers
            if os.path.exists(backup_dir) and any(os.scandir(backup_dir)):
                shutil.make_archive(backup_file.replace('.zip', ''), 'zip', backup_dir)
                # Limpar pasta temporária
                shutil.rmtree(backup_dir)
                return True, f"✓ Backup de drivers concluído: {backup_file}"
            else:
                return False, "Nenhum driver foi exportado"
        else:
            return False, f"Erro ao exportar drivers: {result.stderr}"
        
    except Exception as e:
        return False, f"Erro ao fazer backup de drivers: {e}"