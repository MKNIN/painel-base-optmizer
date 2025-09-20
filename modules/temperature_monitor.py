import os
import subprocess
from colorama import Fore, Style

def execute():
    """Monitorar temperatura do sistema"""
    try:
        print("Verificando temperatura do sistema...")
        
        # Tentar obter informações de temperatura
        temp_info = ""
        try:
            # Usar PowerShell para tentar obter temperatura
            ps_command = '''
            Get-WmiObject -Namespace "root\\wmi" -Class MSAcpi_ThermalZoneTemperature | 
            ForEach-Object { 
                $temp = ($_.CurrentTemperature / 10) - 273.15
                "Temperatura: {0:N1}°C" -f $temp
            }
            '''
            result = subprocess.run(['powershell', '-Command', ps_command], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and result.stdout.strip():
                temp_info = f"\nTemperaturas do sistema:\n{result.stdout}"
            else:
                temp_info = "\nNão foi possível obter informações de temperatura\n"
                temp_info += "Alguns sistemas não expõem dados de temperatura via WMI"
                
        except subprocess.TimeoutExpired:
            temp_info = "\nTempo limite excedido ao obter temperatura"
        except Exception as e:
            temp_info = f"\nErro ao obter temperatura: {e}"
        
        return True, f"Verificação de temperatura concluída.{temp_info}"
        
    except Exception as e:
        return False, f"Erro ao verificar temperatura: {e}"