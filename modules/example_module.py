import os
import subprocess
from colorama import Fore, Style

def execute():
    """Exemplo de módulo personalizado"""
    try:
        print("Executando módulo de exemplo...")
        
        # Verificar espaço em disco de forma mais robusta
        disk_info = ""
        try:
            # Usar PowerShell para obter informações de disco de forma mais confiável
            ps_command = 'Get-PSDrive C | Select-Object Used, Free, @{Name="Total";Expression={$_.Used + $_.Free}} | Format-List'
            result = subprocess.run(['powershell', '-Command', ps_command], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                disk_info = f"\nInformações do disco C:\:\n{result.stdout}"
            else:
                disk_info = "\nNão foi possível obter informações do disco"
                
        except subprocess.TimeoutExpired:
            disk_info = "\nTempo limite excedido ao obter informações do disco"
        except Exception as e:
            disk_info = f"\nErro ao obter informações do disco: {e}"
        
        return True, f"Módulo executado com sucesso!{disk_info}"
        
    except Exception as e:
        return False, f"Erro ao executar módulo: {e}"