import os
import subprocess
from colorama import Fore, Style

def execute():
    """Otimizar configurações para SSD"""
    try:
        print("Otimizando configurações para SSD...")
        
        # Comandos de otimização para SSD
        optimizations = [
            ('fsutil behavior set disabledeletenotify 0', 'Desativar notificações de delete'),
            ('powercfg -h off', 'Desativar hibernação'),
            ('defrag C: /O', 'Otimizar unidades SSD'),
        ]
        
        results = []
        for cmd, description in optimizations:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    results.append(f"✓ {description}")
                else:
                    results.append(f"⚠ {description}: {result.stderr}")
            except Exception as e:
                results.append(f"✗ {description}: {e}")
        
        return True, "Otimizações para SSD aplicadas:\n" + "\n".join(results)
        
    except Exception as e:
        return False, f"Erro ao otimizar SSD: {e}"