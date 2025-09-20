import os
import subprocess
from colorama import Fore, Style

def execute():
    """Limpar logs do sistema"""
    try:
        print("Limpando logs do sistema...")
        
        # Limpar logs de eventos (requer permissões administrativas)
        commands = [
            'wevtutil el | foreach {wevtutil cl "$_"}',
            'del /q /f %SystemRoot%\\System32\\Winevt\\Logs\\*.*',
            'del /q /f %SystemRoot%\\Logs\\*.*'
        ]
        
        results = []
        for cmd in commands:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    results.append(f"✓ Comando executado: {cmd}")
                else:
                    results.append(f"⚠ Erro no comando {cmd}: {result.stderr}")
            except Exception as e:
                results.append(f"✗ Exceção no comando {cmd}: {e}")
        
        return True, "Limpeza de logs concluída:\n" + "\n".join(results)
        
    except Exception as e:
        return False, f"Erro ao limpar logs: {e}"