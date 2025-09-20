import os
import subprocess
from colorama import Fore, Style

def execute():
    """Verificar configurações de segurança"""
    try:
        print("Verificando configurações de segurança...")
        
        checks = []
        
        # Verificar se Windows Defender está ativo
        try:
            result = subprocess.run('sc query WinDefend', shell=True, capture_output=True, text=True)
            if "RUNNING" in result.stdout:
                checks.append("✓ Windows Defender está ativo")
            else:
                checks.append("⚠ Windows Defender não está em execução")
        except:
            checks.append("✗ Não foi possível verificar Windows Defender")
        
        # Verificar firewall
        try:
            result = subprocess.run('netsh advfirewall show allprofiles state', shell=True, capture_output=True, text=True)
            if "ON" in result.stdout:
                checks.append("✓ Firewall está ativo")
            else:
                checks.append("⚠ Firewall não está ativo")
        except:
            checks.append("✗ Não foi possível verificar firewall")
        
        # Verificar UAC
        try:
            result = subprocess.run('reg query HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA', 
                                  shell=True, capture_output=True, text=True)
            if "0x1" in result.stdout:
                checks.append("✓ UAC (Controle de Conta de Usuário) está ativo")
            else:
                checks.append("⚠ UAC não está ativo")
        except:
            checks.append("✗ Não foi possível verificar UAC")
        
        return True, "Verificação de segurança concluída:\n" + "\n".join(checks)
        
    except Exception as e:
        return False, f"Erro na verificação de segurança: {e}"