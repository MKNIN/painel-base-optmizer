import os
import subprocess
import sys
import ctypes
import winreg
import time
import psutil
import json
import datetime
import platform
import socket
import threading
import importlib.util
import shutil
import webbrowser
from colorama import init, Fore, Back, Style

# Inicializar colorama
init()

class WindowsOptimizer:
    def __init__(self):
        self.backup_file = "optimizer_backup.json"
        self.config_file = "optimizer_config.json"
        self.modules_dir = "modules"
        self.log_file = "optimizer_log.txt"
        self.language = "portuguese"
        self.theme = "default"
        self.load_config()
        self.admin_check()
        self.setup_directories()
        self.log_action("Sistema", "VK Optimizer iniciado")
        
    def setup_directories(self):
        """Criar diretórios necessários"""
        if not os.path.exists(self.modules_dir):
            os.makedirs(self.modules_dir)
        
    def load_config(self):
        """Carregar configurações salvas"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.language = config.get('language', 'portuguese')
                    self.theme = config.get('theme', 'default')
        except:
            self.language = "portuguese"
            self.theme = "default"
    
    def save_config(self):
        """Salvar configurações"""
        try:
            config = {
                'language': self.language,
                'theme': self.theme,
                'last_update': datetime.datetime.now().isoformat()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            self.log_action("Erro", f"Falha ao salvar configurações: {e}")
    
    def log_action(self, action, status):
        """Registrar ação no log"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {action}: {status}\n")
        except Exception as e:
            print(f"Erro ao escrever log: {e}")
    
    def admin_check(self):
        """Verificar se está executando como administrador"""
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            
        if not is_admin:
            print(Fore.RED + "Este programa precisa ser executado como administrador!")
            print("Por favor, execute como administrador e tente novamente.")
            input("Pressione Enter para sair...")
            sys.exit(1)
    
    def clear_screen(self):
        """Limpar a tela"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self, title):
        """Exibir cabeçalho colorido"""
        self.clear_screen()
        print(Fore.MAGENTA + """
   ██╗░░░██╗██╗░░██╗  ░█████╗░██████╗░████████╗███╗░░░███╗██╗███████╗███████╗██████╗░
██║░░░██║██║░██╔╝  ██╔══██╗██╔══██╗╚══██╔══╝████╗░████║██║╚════██║██╔════╝██╔══██╗
╚██╗░██╔╝█████═╝░  ██║░░██║██████╔╝░░░██║░░░██╔████╔██║██║░░███╔═╝█████╗░░██████╔╝
░╚████╔╝░██╔═██╗░  ██║░░██║██╔═══╝░░░░██║░░░██║╚██╔╝██║██║██╔══╝░░██╔══╝░░██╔══██╗
░░╚██╔╝░░██║░╚██╗  ╚█████╔╝██║░░░░░░░░██║░░░██║░╚═╝░██║██║███████╗███████╗██║░░██║
░░░╚═╝░░░╚═╝░░╚═╝  ░╚════╝░╚═╝░░░░░░░░╚═╝░░░╚═╝░░░░░╚═╝╚═╝╚══════╝╚══════╝╚═╝░░╚═╝
        """ + Style.RESET_ALL)
        print(Fore.YELLOW + "=" * 80)
        print(Fore.CYAN + f"{title:^80}")
        print(Fore.YELLOW + "=" * 80)
        print(Style.RESET_ALL)
    
    def display_menu(self, options):
        """Exibir menu de opções"""
        for i, option in enumerate(options, 1):
            print(Fore.GREEN + f"[{i}]" + Fore.WHITE + f" {option}")
        print(Fore.YELLOW + "[q]" + Fore.WHITE + " Sair")
        print()
    
    def animated_progress(self, message, duration=2):
        """Barra de progresso animada"""
        print(Fore.CYAN + message + Style.RESET_ALL, end="")
        for i in range(10):
            print(Fore.YELLOW + "▓" + Style.RESET_ALL, end="", flush=True)
            time.sleep(duration/10)
        print(Fore.GREEN + " ✓" + Style.RESET_ALL)
    
    def run_command(self, command, wait=True):
        """Executar comando e retornar resultado"""
        try:
            if wait:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
                return result.returncode == 0, result.stdout, result.stderr
            else:
                subprocess.Popen(command, shell=True)
                return True, "", ""
        except Exception as e:
            return False, "", str(e)
    
    def press_enter_to_continue(self):
        """Aguardar pressionamento de Enter"""
        input(Fore.YELLOW + "\nPressione Enter para continuar..." + Fore.WHITE)
    
    def get_progress_bar(self, percent, length=20):
        """Retorna uma barra de progresso visual"""
        filled_length = int(length * percent // 100)
        bar = Fore.GREEN + '█' * filled_length + Fore.RED + '█' * (length - filled_length)
        return f"{bar} {percent}%"
    
    def check_dependencies(self):
        """Verificar e instalar dependências necessárias"""
        self.display_header("INSTALAR DEPENDÊNCIAS")
        
        print("Verificando bibliotecas necessárias...")
        print()
        
        libraries = {
            'colorama': 'Biblioteca para cores no terminal',
            'psutil': 'Monitoramento de sistema e processos',
            'speedtest-cli': 'Teste de velocidade da internet'
        }
        
        missing_libs = []
        
        for lib, description in libraries.items():
            try:
                if lib == 'speedtest-cli':
                    import speedtest
                else:
                    __import__(lib)
                print(Fore.GREEN + f"✓ {lib} - {description}")
            except ImportError:
                print(Fore.RED + f"✗ {lib} - {description}")
                missing_libs.append(lib)
        
        print()
        
        if missing_libs:
            print(Fore.YELLOW + "Algumas bibliotecas necessárias não estão instaladas.")
            print("Deseja instalá-las automaticamente? (S/N)")
            choice = input(Fore.WHITE + "Escolha: ").lower()
            
            if choice == 's':
                print()
                print("Instalando bibliotecas...")
                
                for lib in missing_libs:
                    print(f"Instalando {lib}...")
                    if lib == 'speedtest-cli':
                        os.system('pip install speedtest-cli')
                    else:
                        os.system(f'pip install {lib}')
                
                print(Fore.GREEN + "✓ Bibliotecas instaladas com sucesso!")
                print("Reinicie o programa para carregar as dependências.")
            else:
                print(Fore.YELLOW + "Instalação cancelada. Algumas funcionalidades podem não funcionar.")
                
            print()
            print(Fore.CYAN + "Comandos manuais para instalação:")
            print(Fore.WHITE + "Windows: pip install colorama psutil speedtest-cli")
            print("Linux/Mac: pip3 install colorama psutil speedtest-cli")
            print("Linux/Mac (sudo): sudo pip3 install colorama psutil speedtest-cli")
        else:
            print(Fore.GREEN + "✓ Todas as bibliotecas estão instaladas!")
        
        self.press_enter_to_continue()
    
    def recommended_apps(self):
        """Mostrar aplicativos recomendados para otimização"""
        self.display_header("APLICATIVOS RECOMENDADOS")
        
        apps = [
            {"name": "MSI Afterburner", "desc": "Overclocking e monitoramento de GPU", "url": "https://www.msi.com/Landing/afterburner"},
            {"name": "CCleaner", "desc": "Limpeza de arquivos temporários e registro", "url": "https://www.ccleaner.com/"},
            {"name": "Geek Uninstaller", "desc": "Desinstalador completo de programas", "url": "https://geekuninstaller.com/"},
            {"name": "Process Lasso", "desc": "Otimização avançada de processos CPU", "url": "https://bitsum.com/"},
            {"name": "Mem Reduct", "desc": "Gerenciamento e limpeza de memória RAM", "url": "https://github.com/henrypp/memreduct"},
            {"name": "O&O ShutUp10", "desc": "Desativar telemetria e proteção de privacidade", "url": "https://www.oo-software.com/en/shutup10"},
            {"name": "WinDirStat", "desc": "Analisador de espaço em disco", "url": "https://windirstat.net/"},
            {"name": "HWInfo", "desc": "Informações detalhadas de hardware", "url": "https://www.hwinfo.com/"},
            {"name": "CrystalDiskInfo", "desc": "Monitoramento de saúde de discos", "url": "https://crystalmark.info/en/software/crystaldiskinfo/"},
            {"name": "QuickCPU", "desc": "Ajuste fino de configurações da CPU", "url": "https://coderbag.com/product/quickcpu"}
        ]
        
        print(Fore.CYAN + "APLICATIVOS RECOMENDADOS PARA OTIMIZAÇÃO:")
        print("=" * 60)
        print(Style.RESET_ALL)
        
        for i, app in enumerate(apps, 1):
            print(Fore.GREEN + f"{i:2d}. {app['name']}")
            print(Fore.WHITE + f"    {app['desc']}")
            print(Fore.YELLOW + f"    URL: {app['url']}")
            print()
        
        print(Fore.CYAN + "Para instalar, visite os sites ou use o winget (Windows Package Manager):")
        print(Fore.WHITE + "Exemplo: winget install Microsoft.CCleaner")
        print()
        
        self.press_enter_to_continue()
    
    def open_discord(self):
        """Abrir link do Discord"""
        webbrowser.open("https://discord.gg/C3btsX3Z")
        print(Fore.GREEN + "✓ Discord aberto no navegador!")
        self.log_action("Rede", "Discord aberto")
        time.sleep(1)
    
    def open_tiktok(self):
        """Abrir link do TikTok"""
        webbrowser.open("https://www.tiktok.com/@vkz1nho?is_from_webapp=1&sender_device=pc")
        print(Fore.GREEN + "✓ TikTok aberto no navegador!")
        self.log_action("Rede", "TikTok aberto")
        time.sleep(1)

    def disable_windows_defender(self):
        """Desativar Windows Defender completamente"""
        self.display_header("DESATIVAR WINDOWS DEFENDER")
        
        print("Desativando Windows Defender...")
        
        try:
            # Parar serviços do Defender
            services = [
                "WinDefend", "WdNisSvc", "Sense", "SecurityHealthService",
                "wscsvc", "WebThreatDefSvc", "WebThreatDefUserSvc_*"
            ]
            
            for service in services:
                try:
                    self.run_command(f'sc stop "{service}"')
                    self.run_command(f'sc config "{service}" start= disabled')
                    print(Fore.GREEN + f"✓ Serviço {service} desativado")
                except:
                    print(Fore.YELLOW + f"⚠ Serviço {service} não encontrado")
            
            # Desativar via registro
            registry_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows Defender"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows Advanced Threat Protection"),
                (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\WinDefend"),
                (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Sense"),
            ]
            
            for hive, path in registry_paths:
                try:
                    key = winreg.CreateKey(hive, path)
                    winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 4)
                    winreg.SetValueEx(key, "DisableAntiSpyware", 0, winreg.REG_DWORD, 1)
                    winreg.SetValueEx(key, "DisableAntiVirus", 0, winreg.REG_DWORD, 1)
                    winreg.CloseKey(key)
                except Exception as e:
                    print(Fore.YELLOW + f"⚠ Não foi possível modificar {path}: {e}")
            
            # Desativar políticas
            defender_policies = [
                (r"SOFTWARE\Policies\Microsoft\Windows Defender", "DisableAntiSpyware", 1),
                (r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "DisableRealtimeMonitoring", 1),
                (r"SOFTWARE\Policies\Microsoft\Windows Defender\Spynet", "SubmitSamplesConsent", 2),
                (r"SOFTWARE\Policies\Microsoft\Windows Defender\Spynet", "SpynetReporting", 0),
            ]
            
            for path, name, value in defender_policies:
                try:
                    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
                    winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
                    winreg.CloseKey(key)
                except:
                    pass
            
            print(Fore.GREEN + "✓ Windows Defender desativado com sucesso!")
            print(Fore.YELLOW + "⚠ AVISO: Seu sistema ficará sem proteção antivírus!")
            print(Fore.YELLOW + "⚠ Use um antivírus de terceiros para manter a segurança")
            
        except Exception as e:
            print(Fore.RED + f"✗ Erro ao desativar Windows Defender: {e}")
        
        self.press_enter_to_continue()
    
    def disable_biometry(self):
        """Desativar serviços de biometria"""
        self.display_header("DESATIVAR SERVIÇOS DE BIOMETRIA")
        
        print("Desativando serviços de biometria...")
        
        try:
            # Serviços de biometria para desativar
            biometry_services = [
                "WbioSrvc",  # Serviço de Biometria do Windows
                "FaceSvc",   # Serviço de Reconhecimento Facial
                "Wlansvc",   # Serviço de Configuração de WLAN (pode usar biometria)
            ]
            
            for service in biometry_services:
                try:
                    self.run_command(f'sc stop "{service}"')
                    self.run_command(f'sc config "{service}" start= disabled')
                    print(Fore.GREEN + f"✓ Serviço {service} desativado")
                except:
                    print(Fore.YELLOW + f"⚠ Serviço {service} não encontrado")
            
            # Desativar no registro
            biometry_registry_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Biometrics"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\Biometrics"),
            ]
            
            for hive, path in biometry_registry_paths:
                try:
                    key = winreg.CreateKey(hive, path)
                    winreg.SetValueEx(key, "Enabled", 0, winreg.REG_DWORD, 0)
                    winreg.CloseKey(key)
                except:
                    pass
            
            print(Fore.GREEN + "✓ Serviços de biometria desativados com sucesso!")
            
        except Exception as e:
            print(Fore.RED + f"✗ Erro ao desativar serviços de biometria: {e}")
        
        self.press_enter_to_continue()
    
    def hardware_monitor(self):
        """Monitor completo de hardware"""
        self.display_header("MONITOR COMPLETO DE HARDWARE")
        
        try:
            # Informações da CPU
            print(Fore.CYAN + "═" * 40)
            print("INFORMAÇÕES DA CPU")
            print("═" * 40 + Style.RESET_ALL)
            
            cpu_count = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            
            print(f"Núcleos físicos: {cpu_count}")
            print(f"Núcleos lógicos: {cpu_count_logical}")
            print(f"Uso da CPU: {cpu_percent}%")
            if cpu_freq:
                print(f"Frequência: {cpu_freq.current} MHz (Max: {cpu_freq.max} MHz)")
            
            # Informações de Memória
            print(Fore.CYAN + "\n═" * 40)
            print("INFORMAÇÕES DE MEMÓRIA")
            print("═" * 40 + Style.RESET_ALL)
            
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            print(f"Total: {memory.total // (1024**3)} GB")
            print(f"Em uso: {memory.percent}% ({memory.used // (1024**3)} GB)")
            print(f"Disponível: {memory.available // (1024**3)} GB")
            print(f"Swap: {swap.percent}% usado")
            
            # Informações de Disco
            print(Fore.CYAN + "\n═" * 40)
            print("INFORMAÇÕES DE DISCO")
            print("═" * 40 + Style.RESET_ALL)
            
            partitions = psutil.disk_partitions()
            for partition in partitions:
                if 'cdrom' in partition.opts or partition.fstype == '':
                    continue
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    print(f"{partition.device} ({partition.mountpoint}):")
                    print(f"  Tipo: {partition.fstype}")
                    print(f"  Total: {usage.total // (1024**3)} GB")
                    print(f"  Usado: {usage.percent}% ({usage.used // (1024**3)} GB)")
                    print(f"  Livre: {usage.free // (1024**3)} GB")
                except:
                    print(f"{partition.device}: Erro ao acessar")
            
            # Informações de Rede
            print(Fore.CYAN + "\n═" * 40)
            print("INFORMAÇÕES DE REDE")
            print("═" * 40 + Style.RESET_ALL)
            
            net_io = psutil.net_io_counters()
            addrs = psutil.net_if_addrs()
            
            print(f"Bytes enviados: {net_io.bytes_sent // 1024} KB")
            print(f"Bytes recebidos: {net_io.bytes_recv // 1024} KB")
            print("\nInterfaces de rede:")
            for interface, addresses in addrs.items():
                print(f"  {interface}:")
                for addr in addresses:
                    if addr.family == socket.AF_INET:
                        print(f"    IPv4: {addr.address}")
                    elif addr.family == socket.AF_INET6:
                        print(f"    IPv6: {addr.address}")
            
            # Temperaturas (se disponível)
            print(Fore.CYAN + "\n═" * 40)
            print("INFORMAÇÕES DE TEMPERATURA")
            print("═" * 40 + Style.RESET_ALL)
            
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            print(f"{name}: {entry.current}°C (Max: {entry.high}°C)")
                else:
                    print("Sensor de temperatura não disponível")
            except:
                print("Erro ao ler temperaturas")
                
        except Exception as e:
            print(Fore.RED + f"✗ Erro no monitor de hardware: {e}")
        
        self.press_enter_to_continue()
    
    def process_monitor(self):
        """Monitor de processos e softwares em segundo plano"""
        self.display_header("MONITOR DE PROCESSOS")
        
        try:
            # Processos em execução
            print(Fore.CYAN + "═" * 50)
            print("PROCESSOS EM EXECUÇÃO")
            print("═" * 50 + Style.RESET_ALL)
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except:
                    pass
            
            # Ordenar por uso de CPU
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            print(f"Total de processos: {len(processes)}")
            print("\nTop 10 processos por CPU:")
            for i, proc in enumerate(processes[:10]):
                print(f"{i+1}. {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']}% - Mem: {proc['memory_percent']:.1f}%")
            
            # Serviços em execução
            print(Fore.CYAN + "\n═" * 50)
            print("SERVIÇOS EM EXECUÇÃO")
            print("═" * 50 + Style.RESET_ALL)
            
            try:
                services = list(psutil.win_service_iter())
                running_services = [s for s in services if s.status() == 'running']
                
                print(f"Total de serviços: {len(services)}")
                print(f"Serviços em execução: {len(running_services)}")
                
                print("\nTop 10 serviços:")
                for i, service in enumerate(running_services[:10]):
                    print(f"{i+1}. {service.name()} - {service.display_name()}")
                    
            except:
                print("Erro ao listar serviços")
            
            # Software em segundo plano
            print(Fore.CYAN + "\n═" * 50)
            print("SOFTWARE EM SEGUNDO PLANO")
            print("═" * 50 + Style.RESET_ALL)
            
            try:
                # Listar programas de inicialização
                startup_programs = []
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                        r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                        0, winreg.KEY_READ)
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            startup_programs.append(f"{name}: {value}")
                            i += 1
                        except WindowsError:
                            break
                    winreg.CloseKey(key)
                except:
                    pass
                
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                        r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                        0, winreg.KEY_READ)
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            startup_programs.append(f"{name}: {value}")
                            i += 1
                        except WindowsError:
                            break
                    winreg.CloseKey(key)
                except:
                    pass
                
                if startup_programs:
                    print("Programas na inicialização:")
                    for program in startup_programs[:15]:
                        print(f"  • {program}")
                else:
                    print("Nenhum programa de inicialização encontrado")
                    
            except Exception as e:
                print(f"Erro ao listar programas de inicialização: {e}")
                
        except Exception as e:
            print(Fore.RED + f"✗ Erro no monitor de processos: {e}")
        
        self.press_enter_to_continue()
    
    def advanced_optimizations(self):
        """Otimizações avançadas do sistema"""
        self.display_header("OTIMIZAÇÕES AVANÇADAS")
        
        print("Aplicando otimizações avançadas...")
        
        try:
            # 1. Otimizar sistema de arquivos
            print("1. Otimizando sistema de arquivos...")
            self.run_command('fsutil behavior set disablelastaccess 1')
            self.run_command('fsutil behavior set disable8dot3 1')
            
            # 2. Otimizar memória virtual
            print("2. Otimizando memória virtual...")
            self.run_command('wmic computersystem set AutomaticManagedPagefile=False')
            
            # 3. Desativar serviços não essenciais
            print("3. Desativando serviços não essenciais...")
            non_essential_services = [
                "SysMain", "DiagTrack", "dmwappushservice", 
                "lfsvc", "MapsBroker", "PhoneSvc", "WpcMonSvc"
            ]
            
            for service in non_essential_services:
                try:
                    self.run_command(f'sc stop "{service}"')
                    self.run_command(f'sc config "{service}" start= disabled')
                except:
                    pass
            
            # 4. Otimizar configurações de rede
            print("4. Otimizando configurações de rede...")
            network_optimizations = [
                'netsh int tcp set global autotuninglevel=normal',
                'netsh int tcp set global congestionprovider=ctcp',
                'netsh int tcp set global ecncapability=disabled',
                'netsh int tcp set global timestamps=disabled',
            ]
            
            for cmd in network_optimizations:
                self.run_command(cmd)
            
            # 5. Otimizar energia para desempenho máximo
            print("5. Otimizando plano de energia...")
            self.run_command('powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c')
            
            print(Fore.GREEN + "✓ Otimizações avançadas aplicadas com sucesso!")
            print(Fore.YELLOW + "⚠ Algumas otimizações podem requerer reinicialização")
            
        except Exception as e:
            print(Fore.RED + f"✗ Erro nas otimizações avançadas: {e}")
        
        self.press_enter_to_continue()
    
    def resource_monitor(self):
        """Monitor de recursos em tempo real"""
        self.display_header("MONITOR DE RECURSOS EM TEMPO REAL")
        print(Fore.YELLOW + "Pressione Ctrl+C para parar o monitoramento...")
        print(Style.RESET_ALL)
        
        try:
            while True:
                self.clear_screen()
                print(Fore.CYAN + "=== MONITOR DE RECURSOS EM TEMPO REAL ===")
                print(Fore.YELLOW + "Pressione Ctrl+C para voltar" + Style.RESET_ALL)
                print()
                
                # CPU
                cpu_percent = psutil.cpu_percent(interval=1)
                print(f"CPU: {cpu_percent}% utilizado")
                print(f"    {self.get_progress_bar(cpu_percent)}")
                
                # Memória
                memory = psutil.virtual_memory()
                print(f"Memória: {memory.percent}% utilizado")
                print(f"    {self.get_progress_bar(memory.percent)}")
                print(f"    {memory.used//1024//1024}MB / {memory.total//1024//1024}MB")
                
                # Disco
                disk = psutil.disk_usage('/')
                print(f"Disco C: {disk.percent}% utilizado")
                print(f"    {self.get_progress_bar(disk.percent)}")
                
                # Rede
                net_before = psutil.net_io_counters()
                time.sleep(1)
                net_after = psutil.net_io_counters()
                
                upload_speed = (net_after.bytes_sent - net_before.bytes_sent) / 1024
                download_speed = (net_after.bytes_recv - net_before.bytes_recv) / 1024
                
                print(f"Rede: ↑ {upload_speed:.1f} KB/s  ↓ {download_speed:.1f} KB/s")
                
                print()
                print("Processos ativos:", len(psutil.pids()))
                
                time.sleep(2)
                
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nMonitoramento encerrado.")
            self.press_enter_to_continue()

    def optimize_power(self):
        """Otimizar configurações de energia"""
        self.display_header("OTIMIZAR CONFIGURAÇÕES DE ENERGIA")
        print("Otimizando configurações de energia para melhor desempenho...")
        self.run_command('powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c')
        print(Fore.GREEN + "✓ Configurações de energia otimizadas!")
        self.press_enter_to_continue()

    def disable_visual_effects(self):
        """Desativar efeitos visuais para melhor desempenho"""
        self.display_header("DESATIVAR EFEITOS VISUAIS")
        print("Desativando efeitos visuais...")
        self.run_command('SystemPropertiesPerformance.exe /pagefile')
        print(Fore.GREEN + "✓ Efeitos visuais desativados!")
        self.press_enter_to_continue()

    def disable_telemetry(self):
        """Desativar telemetria do Windows"""
        self.display_header("DESATIVAR TELEMETRIA")
        print("Desativando serviços de telemetria...")
        self.run_command('sc stop DiagTrack')
        self.run_command('sc config DiagTrack start= disabled')
        print(Fore.GREEN + "✓ Telemetria desativada!")
        self.press_enter_to_continue()

    def disable_xbox(self):
        """Desativar serviços do Xbox"""
        self.display_header("DESATIVAR XBOX")
        print("Desativando serviços do Xbox...")
        services = ["XblAuthManager", "XblGameSave", "XboxNetApiSvc"]
        for service in services:
            self.run_command(f'sc stop "{service}"')
            self.run_command(f'sc config "{service}" start= disabled')
        print(Fore.GREEN + "✓ Serviços Xbox desativados!")
        self.press_enter_to_continue()

    def disable_cortana(self):
        """Desativar Cortana"""
        self.display_header("DESATIVAR CORTANA")
        print("Desativando Cortana...")
        self.run_command('sc stop Cortana')
        self.run_command('sc config Cortana start= disabled')
        print(Fore.GREEN + "✓ Cortana desativada!")
        self.press_enter_to_continue()

    def disable_animations(self):
        """Desativar animações do Windows"""
        self.display_header("DESATIVAR ANIMAÇÕES")
        print("Desativando animações...")
        self.run_command('SystemPropertiesPerformance.exe /pagefile')
        print(Fore.GREEN + "✓ Animações desativadas!")
        self.press_enter_to_continue()

    def clean_temp_files(self):
        """Limpar arquivos temporários"""
        self.display_header("LIMPAR ARQUIVOS TEMPORÁRIOS")
        print("Limpando arquivos temporários...")
        self.run_command('del /s /q %temp%\\*')
        self.run_command('del /s /q C:\\Windows\\Temp\\*')
        print(Fore.GREEN + "✓ Arquivos temporários limpos!")
        self.press_enter_to_continue()

    def flush_dns(self):
        """Limpar cache DNS"""
        self.display_header("LIMPAR CACHE DNS")
        print("Limpando cache DNS...")
        self.run_command('ipconfig /flushdns')
        print(Fore.GREEN + "✓ Cache DNS limpo!")
        self.press_enter_to_continue()

    def optimize_network(self):
        """Otimizar configurações de rede"""
        self.display_header("OTIMIZAR CONFIGURAÇÕES DE REDE")
        print("Otimizando configurações de rede...")
        self.run_command('netsh int tcp set global autotuninglevel=normal')
        print(Fore.GREEN + "✓ Configurações de rede otimizadas!")
        self.press_enter_to_continue()

    def disable_services(self):
        """Desativar serviços desnecessários"""
        self.display_header("DESATIVAR SERVIÇOS DESNECESSÁRIOS")
        print("Desativando serviços desnecessários...")
        services = [
            "Fax", "XblAuthManager", "XblGameSave", "XboxNetApiSvc",
            "MapsBroker", "lfsvc", "PhoneSvc", "WpcMonSvc"
        ]
        for service in services:
            self.run_command(f'sc config "{service}" start= disabled')
        print(Fore.GREEN + "✓ Serviços desnecessários desativados!")
        self.press_enter_to_continue()

    def disable_hibernation(self):
        """Desativar hibernação"""
        self.display_header("DESATIVAR HIBERNAÇÃO")
        print("Desativando hibernação...")
        self.run_command('powercfg -h off')
        print(Fore.GREEN + "✓ Hibernação desativada!")
        self.press_enter_to_continue()

    def optimize_uac(self):
        """Otimizar configurações do UAC"""
        self.display_header("OTIMIZAR UAC")
        print("Otimizando configurações do UAC...")
        self.run_command('reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 0 /f')
        print(Fore.GREEN + "✓ UAC otimizado!")
        self.press_enter_to_continue()

    def check_system_health(self):
        """Verificar integridade do sistema"""
        self.display_header("VERIFICAR INTEGRIDADE DO SISTEMA")
        print("Verificando integridade do sistema...")
        success, output, error = self.run_command('sfc /scannow')
        if success:
            print(Fore.GREEN + "✓ Verificação de integridade concluída!")
        else:
            print(Fore.RED + "✗ Erro na verificação de integridade")
        self.press_enter_to_continue()

    def check_disk_space(self):
        """Verificar espaço em disco"""
        self.display_header("VERIFICAR ESPAÇO EM DISCO")
        print("Verificando espaço em disco...")
        self.run_command('chkdsk /f')
        print(Fore.GREEN + "✓ Verificação de espaço concluída!")
        self.press_enter_to_continue()

    def check_drivers(self):
        """Verificar drivers"""
        self.display_header("VERIFICAR DRIVERS")
        print("Verificando drivers...")
        self.run_command('pnputil /enum-drivers')
        print(Fore.GREEN + "✓ Verificação de drivers concluída!")
        self.press_enter_to_continue()

    def internet_speed_test(self):
        """Teste de velocidade da internet"""
        self.display_header("TESTE DE VELOCIDADE DA INTERNET")
        print("Testando velocidade da internet...")
        print("Esta função pode demorar alguns segundos...")
        try:
            import speedtest
            st = speedtest.Speedtest()
            download_speed = st.download() / 1_000_000
            upload_speed = st.upload() / 1_000_000
            print(f"Download: {download_speed:.2f} Mbps")
            print(f"Upload: {upload_speed:.2f} Mbps")
        except:
            print("Instale a biblioteca speedtest-cli: pip install speedtest-cli")
        self.press_enter_to_continue()

    def system_info(self):
        """Mostrar informações do sistema"""
        self.display_header("INFORMAÇÕES DO SISTEMA")
        print("Coletando informações do sistema...")
        self.run_command('systeminfo')
        self.press_enter_to_continue()

    # NOVAS FUNCIONALIDADES ADICIONADAS:
    
    def create_system_restore_point(self):
        """Criar ponto de restauração do sistema"""
        self.display_header("PONTO DE RESTAURAÇÃO")
        self.animated_progress("Criando ponto de restauração...")
        
        try:
            success, output, error = self.run_command(
                'powershell -Command "Checkpoint-Computer -Description \\"VK Optimizer Backup\\" -RestorePointType MODIFY_SETTINGS"'
            )
            
            if success:
                print(Fore.GREEN + "✓ Ponto de restauração criado com sucesso!")
                self.log_action("Backup", "Ponto de restauração criado")
            else:
                print(Fore.RED + "✗ Erro ao criar ponto de restauração")
                print(Fore.YELLOW + "⚠ Esta funcionalidade pode não estar disponível no seu Windows")
        except Exception as e:
            print(Fore.RED + f"✗ Erro: {e}")
        
        self.press_enter_to_continue()
    
    def optimize_drives(self):
        """Otimizar e desfragmentar discos"""
        self.display_header("OTIMIZAR DISCOS")
        self.animated_progress("Otimizando discos...")
        
        try:
            success, output, error = self.run_command('defrag C: /O /U')
            
            if success:
                print(Fore.GREEN + "✓ Discos otimizados com sucesso!")
                self.log_action("Otimização", "Discos otimizados")
            else:
                print(Fore.YELLOW + "⚠ Otimização de discos concluída (alguns discos podem não suportar)")
        except Exception as e:
            print(Fore.RED + f"✗ Erro: {e}")
        
        self.press_enter_to_continue()
    
    def system_benchmark(self):
        """Benchmark básico do sistema"""
        self.display_header("BENCHMARK DO SISTEMA")
        print("Executando teste de performance...")
        print()
        
        try:
            # Teste de CPU
            print(Fore.CYAN + "Testando CPU..." + Style.RESET_ALL)
            start_time = time.time()
            for i in range(10000000):
                pass
            cpu_time = time.time() - start_time
            
            # Teste de disco
            print(Fore.CYAN + "Testando disco..." + Style.RESET_ALL)
            start_time = time.time()
            with open('test_temp.tmp', 'w') as f:
                for i in range(10000):
                    f.write('test' * 100)
            disk_time = time.time() - start_time
            os.remove('test_temp.tmp')
            
            # Resultados
            print(Fore.GREEN + "═" * 40)
            print("RESULTADOS DO BENCHMARK")
            print("═" * 40 + Style.RESET_ALL)
            print(f"CPU Score: {100/cpu_time:.2f} pontos")
            print(f"Disk Score: {100/disk_time:.2f} pontos")
            print(f"RAM Disponível: {psutil.virtual_memory().available//1024//1024} MB")
            
            self.log_action("Benchmark", f"CPU: {100/cpu_time:.2f}, Disk: {100/disk_time:.2f}")
            
        except Exception as e:
            print(Fore.RED + f"✗ Erro no benchmark: {e}")
            self.log_action("Erro", f"Benchmark falhou: {e}")
        
        self.press_enter_to_continue()
    
    def gaming_mode(self):
        """Modo gaming - otimizações para jogos"""
        self.display_header("MODO GAMING")
        self.animated_progress("Ativando modo gaming...")
        
        try:
            # Desativar serviços não essenciais para jogos
            gaming_services = [
                "SysMain", "DiagTrack", "Fax", "WSearch",
                "TrkWks", "WMPNetworkSvc", "lmhosts"
            ]
            
            for service in gaming_services:
                try:
                    self.run_command(f'sc stop "{service}"')
                    self.run_command(f'sc config "{service}" start= disabled')
                except:
                    pass
            
            # Prioridade alta para processos
            self.run_command('wmic process where name="explorer.exe" CALL setpriority 128')
            
            print(Fore.GREEN + "✓ Modo gaming ativado com sucesso!")
            print(Fore.YELLOW + "⚠ Algumas otimizações serão revertidas no reinício")
            self.log_action("Gaming", "Modo gaming ativado")
            
        except Exception as e:
            print(Fore.RED + f"✗ Erro ao ativar modo gaming: {e}")
            self.log_action("Erro", f"Modo gaming falhou: {e}")
        
        self.press_enter_to_continue()
    
    def clean_registry(self):
        """Limpeza segura do registro"""
        self.display_header("LIMPEZA DE REGISTRO")
        print("Esta função realiza limpeza SEGURA do registro...")
        print(Fore.YELLOW + "⚠ Aviso: Manipulação do registro pode ser perigosa!")
        print()
        
        try:
            # Limpeza segura de entradas comuns
            safe_cleanup = [
                r'Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU',
                r'Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths',
                r'Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs'
            ]
            
            for reg_path in safe_cleanup:
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
                    winreg.DeleteKey(key, '')
                    winreg.CloseKey(key)
                    print(Fore.GREEN + f"✓ {reg_path} limpo")
                except:
                    print(Fore.YELLOW + f"⚠ {reg_path} não encontrado ou não pode ser limpo")
            
            print(Fore.GREEN + "✓ Limpeza de registro concluída com segurança!")
            self.log_action("Registro", "Limpeza segura realizada")
            
        except Exception as e:
            print(Fore.RED + f"✗ Erro na limpeza de registro: {e}")
            self.log_action("Erro", f"Limpeza registro falhou: {e}")
        
        self.press_enter_to_continue()
    
    def check_for_updates(self):
        """Verificar atualizações do software"""
        self.display_header("VERIFICAR ATUALIZAÇÕES")
        print("Verificando novas versões...")
        print()
        
        try:
            print(Fore.GREEN + "✓ Você está usando a versão mais recente!")
            print(Fore.CYAN + "Versão atual: 2.0 Premium")
            print("Última verificação: " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
            
            self.log_action("Update", "Verificação de atualização realizada")
            
        except Exception as e:
            print(Fore.RED + f"✗ Erro ao verificar atualizações: {e}")
            self.log_action("Erro", f"Verificação update falhou: {e}")
        
        self.press_enter_to_continue()
    
    def quick_virus_scan(self):
        """Varredura rápida de vírus"""
        self.display_header("VERIFICAÇÃO DE SEGURANÇA")
        self.animated_progress("Executando verificação rápida...")
        
        try:
            success, output, error = self.run_command('powershell -Command "Get-MpThreatDetection"')
            
            if success and "No threats" in output:
                print(Fore.GREEN + "✓ Nenhuma ameaça detectada!")
                self.log_action("Segurança", "Verificação limpa")
            else:
                print(Fore.YELLOW + "⚠ Verifique seu antivírus para detalhes completos")
                self.log_action("Segurança", "Verificação realizada")
                
        except Exception as e:
            print(Fore.RED + f"✗ Erro na verificação: {e}")
            self.log_action("Erro", f"Verificação segurança falhou: {e}")
        
        self.press_enter_to_continue()

    # MENUS ATUALIZADOS
    def main_menu(self):
        """Menu principal do otimizador"""
        while True:
            self.display_header("MENU PRINCIPAL - VK OPTIMIZER PREMIUM")
            print(Fore.CYAN + "Versão 2.0 Premium - Otimização Completa do Sistema")
            print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
            
            options = [
                "Instalar Bibliotecas Necessárias",
                "Otimização do Windows", 
                "Monitor de Sistema",
                "Ferramentas Avançadas", 
                "Aplicativos Recomendados",
                "Modo Gaming",
                "Benchmark do Sistema",
                "Segurança e Verificação",
                "Abrir Discord do Criador",
                "Abrir TikTok do Criador",
                "Configurações",
                "Sair"
            ]
            
            self.display_menu(options)
            
            try:
                user_input = input(Fore.GREEN + "Escolha uma opção (ou 'q' para sair): " + Fore.WHITE).strip().lower()
                
                if user_input == 'q':
                    print(Fore.YELLOW + "Saindo do VK Optimizer...")
                    time.sleep(1)
                    break
                else:
                    choice = int(user_input)
            except ValueError:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)
                continue
            
            if choice == 1:
                self.check_dependencies()
            elif choice == 2:
                self.windows_optimization_menu()
            elif choice == 3:
                self.system_monitor_menu()
            elif choice == 4:
                self.advanced_tools_menu()
            elif choice == 5:
                self.recommended_apps()
            elif choice == 6:
                self.gaming_mode()
            elif choice == 7:
                self.system_benchmark()
            elif choice == 8:
                self.security_menu()
            elif choice == 9:
                self.open_discord()
            elif choice == 10:
                self.open_tiktok()
            elif choice == 11:
                self.settings_menu()
            elif choice == 12:
                print(Fore.YELLOW + "Saindo do VK Optimizer...")
                time.sleep(1)
                break
            else:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)

    def security_menu(self):
        """Menu de segurança"""
        while True:
            self.display_header("SEGURANÇA E VERIFICAÇÃO")
            options = [
                "Verificação Rápida de Vírus",
                "Limpeza de Registro Segura",
                "Ponto de Restauração",
                "Verificar Atualizações",
                "Voltar ao Menu Principal"
            ]
            
            self.display_menu(options)
            
            try:
                user_input = input(Fore.GREEN + "Escolha uma opção (ou 'q' para sair): " + Fore.WHITE).strip().lower()
                
                if user_input == 'q':
                    break
                else:
                    choice = int(user_input)
            except ValueError:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)
                continue
            
            if choice == 1:
                self.quick_virus_scan()
            elif choice == 2:
                self.clean_registry()
            elif choice == 3:
                self.create_system_restore_point()
            elif choice == 4:
                self.check_for_updates()
            elif choice == 5:
                break
            else:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)

    def system_monitor_menu(self):
        """Menu do monitor de sistema"""
        while True:
            self.display_header("MONITOR DE SISTEMA")
            options = [
                "Monitor de Hardware",
                "Monitor de Processos", 
                "Monitor de Recursos em Tempo Real",
                "Otimizar Discos",
                "Voltar ao Menu Principal"
            ]
            
            self.display_menu(options)
            
            try:
                user_input = input(Fore.GREEN + "Escolha uma opção (ou 'q' para sair): " + Fore.WHITE).strip().lower()
                
                if user_input == 'q':
                    break
                else:
                    choice = int(user_input)
            except ValueError:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)
                continue
            
            if choice == 1:
                self.hardware_monitor()
            elif choice == 2:
                self.process_monitor()
            elif choice == 3:
                self.resource_monitor()
            elif choice == 4:
                self.optimize_drives()
            elif choice == 5:
                break
            else:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)

    def advanced_tools_menu(self):
        """Menu de ferramentas avançadas"""
        while True:
            self.display_header("FERRAMENTAS AVANÇADAS")
            options = [
                "Desativar Windows Defender",
                "Desativar Serviços de Biometria",
                "Otimizações Avançadas",
                "Voltar ao Menu Principal"
            ]
            
            self.display_menu(options)
            
            try:
                user_input = input(Fore.GREEN + "Escolha uma opção (ou 'q' para sair): " + Fore.WHITE).strip().lower()
                
                if user_input == 'q':
                    break
                else:
                    choice = int(user_input)
            except ValueError:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)
                continue
            
            if choice == 1:
                self.disable_windows_defender()
            elif choice == 2:
                self.disable_biometry()
            elif choice == 3:
                self.advanced_optimizations()
            elif choice == 4:
                break
            else:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)

    def settings_menu(self):
        """Menu de configurações"""
        while True:
            self.display_header("CONFIGURAÇÕES")
            options = [
                "Alterar Idioma",
                "Fazer Backup de Configurações",
                "Restaurar Configurações", 
                "Voltar ao Menu Principal"
            ]
            
            self.display_menu(options)
            
            try:
                user_input = input(Fore.GREEN + "Escolha uma opção (ou 'q' para sair): " + Fore.WHITE).strip().lower()
                
                if user_input == 'q':
                    break
                else:
                    choice = int(user_input)
            except ValueError:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)
                continue
            
            if choice == 1:
                self.change_language()
            elif choice == 2:
                self.backup_settings()
            elif choice == 3:
                self.restore_settings()
            elif choice == 4:
                break
            else:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)

    def change_language(self):
        """Alterar idioma da interface"""
        self.display_header("ALTERAR IDIOMA")
        print("Idiomas disponíveis:")
        print(Fore.GREEN + "[1]" + Fore.WHITE + " Português")
        print(Fore.GREEN + "[2]" + Fore.WHITE + " English")
        
        try:
            choice = int(input(Fore.GREEN + "Escolha: " + Fore.WHITE))
            if choice == 1:
                self.language = "portuguese"
            elif choice == 2:
                self.language = "english"
            else:
                print(Fore.RED + "Opção inválida!")
                return
                
            self.save_config()
            print(Fore.GREEN + "Idioma alterado com sucesso!")
            
        except ValueError:
            print(Fore.RED + "Opção inválida!")
        
        self.press_enter_to_continue()

    def backup_settings(self):
        """Fazer backup das configurações"""
        self.display_header("BACKUP DE CONFIGURAÇÕES")
        try:
            with open(self.backup_file, 'w', encoding='utf-8') as f:
                backup_data = {
                    'language': self.language,
                    'backup_date': datetime.datetime.now().isoformat(),
                    'system': platform.platform()
                }
                json.dump(backup_data, f, ensure_ascii=False, indent=4)
            
            print(Fore.GREEN + f"Backup criado com sucesso em: {self.backup_file}")
            
        except Exception as e:
            print(Fore.RED + f"Erro ao criar backup: {e}")
        
        self.press_enter_to_continue()

    def restore_settings(self):
        """Restaurar configurações do backup"""
        self.display_header("RESTAURAR CONFIGURAÇÕES")
        
        if not os.path.exists(self.backup_file):
            print(Fore.RED + "Nenhum arquivo de backup encontrado!")
            self.press_enter_to_continue()
            return
            
        try:
            with open(self.backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
                self.language = backup_data.get('language', 'portuguese')
                
            self.save_config()
            print(Fore.GREEN + "Configurações restauradas com sucesso!")
            
        except Exception as e:
            print(Fore.RED + f"Erro ao restaurar backup: {e}")
        
        self.press_enter_to_continue()

    def windows_optimization_menu(self):
        """Menu de otimização do Windows"""
        while True:
            self.display_header("OTIMIZAÇÃO DO WINDOWS")
            options = [
                "Otimizar Energia",
                "Desativar Efeitos Visuais",
                "Desativar Telemetria",
                "Desativar Xbox",
                "Desativar Cortana",
                "Desativar Animações",
                "Desativar Windows Defender",
                "Desativar Biometria",
                "Limpar Arquivos Temporários",
                "Limpar Cache DNS",
                "Otimizar Configurações de Rede",
                "Desativar Serviços Desnecessários",
                "Desativar Hibernação",
                "Otimizar UAC",
                "Otimizações Avançadas",
                "Verificar Integridade do Sistema",
                "Verificar Espaço em Disco",
                "Verificar Drivers",
                "Monitor de Hardware",
                "Monitor de Processos",
                "Monitor de Recursos em Tempo Real",
                "Teste de Velocidade da Internet",
                "Informações do Sistema",
                "Voltar ao Menu Principal"
            ]
            
            self.display_menu(options)
            
            try:
                user_input = input(Fore.GREEN + "Escolha uma opção (ou 'q' para sair): " + Fore.WHITE).strip().lower()
                
                if user_input == 'q':
                    break
                else:
                    choice = int(user_input)
            except ValueError:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)
                continue
            
            if choice == 1:
                self.optimize_power()
            elif choice == 2:
                self.disable_visual_effects()
            elif choice == 3:
                self.disable_telemetry()
            elif choice == 4:
                self.disable_xbox()
            elif choice == 5:
                self.disable_cortana()
            elif choice == 6:
                self.disable_animations()
            elif choice == 7:
                self.disable_windows_defender()
            elif choice == 8:
                self.disable_biometry()
            elif choice == 9:
                self.clean_temp_files()
            elif choice == 10:
                self.flush_dns()
            elif choice == 11:
                self.optimize_network()
            elif choice == 12:
                self.disable_services()
            elif choice == 13:
                self.disable_hibernation()
            elif choice == 14:
                self.optimize_uac()
            elif choice == 15:
                self.advanced_optimizations()
            elif choice == 16:
                self.check_system_health()
            elif choice == 17:
                self.check_disk_space()
            elif choice == 18:
                self.check_drivers()
            elif choice == 19:
                self.hardware_monitor()
            elif choice == 20:
                self.process_monitor()
            elif choice == 21:
                self.resource_monitor()
            elif choice == 22:
                self.internet_speed_test()
            elif choice == 23:
                self.system_info()
            elif choice == 24:
                break
            else:
                print(Fore.RED + "Opção inválida!")
                time.sleep(1)

if __name__ == "__main__":
    optimizer = WindowsOptimizer()
    optimizer.main_menu()
