import ipaddress
import subprocess
import platform
import socket
import concurrent.futures
import re

# Configuración de escaneo
TIMEOUT = 1      # Tiempo de espera para conexiones
MAX_HILOS = 50   # Máximo de hilos en el escaneo de puertos

def detectar_sistema_operativo(ip):
    """Intenta detectar el sistema operativo basado en el TTL de la respuesta ICMP."""
    sistema = platform.system()
    comando = ["ping", "-c", "1", "-W", "1", str(ip)] if sistema == "Linux" else ["ping", "-n", "1", "-w", "500", str(ip)]

    try:
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        salida = resultado.stdout

        # Buscar el TTL en la respuesta
        ttl_match = re.search(r"TTL=(\d+)" if sistema == "Windows" else r"ttl=(\d+)", salida)
        if ttl_match:
            ttl = int(ttl_match.group(1))
            if ttl <= 64:
                return "Linux/Unix/macOS"
            elif ttl <= 128:
                return "Windows"
            else:
                return "Posible router/dispositivo IoT"
    except:
        pass
    return "Desconocido"

def ping_dispositivo(ip):
    """Realiza un ping a la IP para verificar si está activa y detecta el SO."""
    sistema_operativo = detectar_sistema_operativo(ip)

    if sistema_operativo != "Desconocido":
        print(f"[+] Dispositivo activo en: {ip} ({sistema_operativo})")
        return (str(ip), sistema_operativo)
    
    return None

def escanear_puerto(ip, puerto):
    """Escanea un puerto específico en una IP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    try:
        s.connect((ip, puerto))
        print(f"    🔓 Puerto {puerto} abierto en {ip}")

        # Intentar obtener banner
        try:
            banner = s.recv(1024).decode().strip()
            if banner:
                print(f"      📌 Banner: {banner}")
        except:
            pass
    except:
        pass
    finally:
        s.close()

def escanear_puertos(ip, inicio_puerto, fin_puerto):
    """Escanea un rango de puertos en una IP."""
    print(f"\n🔎 Escaneando puertos en {ip}...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_HILOS) as executor:
        for puerto in range(inicio_puerto, fin_puerto + 1):
            executor.submit(escanear_puerto, ip, puerto)

def escanear_red(red, inicio_puerto, fin_puerto):
    """Escanea la red para encontrar dispositivos activos y luego escanea sus puertos."""
    print(f"\n🌐 Escaneando la red {red} para encontrar dispositivos...\n")
    dispositivos_activos = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_HILOS) as executor:
        resultados = executor.map(ping_dispositivo, ipaddress.IPv4Network(red, strict=False).hosts())

    # Filtrar dispositivos activos
    dispositivos_activos = [ip for ip in resultados if ip]

    print("\n✅ Dispositivos activos encontrados:")
    for ip, os in dispositivos_activos:
        print(f"  - {ip} ({os})")

    if dispositivos_activos:
        # Escanear puertos en cada dispositivo
        for ip, _ in dispositivos_activos:
            escanear_puertos(ip, inicio_puerto, fin_puerto)

if __name__ == "__main__":
    red = input("Ingrese la red a escanear (Ejemplo: 192.168.56.0/24): ")
    
    while True:
        try:
            inicio_puerto = int(input("Ingrese el puerto inicial: "))
            fin_puerto = int(input("Ingrese el puerto final: "))
            if 1 <= inicio_puerto <= 65535 and 1 <= fin_puerto <= 65535 and inicio_puerto <= fin_puerto:
                break
            else:
                print("❌ Rango de puertos inválido. Debe estar entre 1 y 65535.")
        except ValueError:
            print("❌ Debe ingresar números válidos.")

    escanear_red(red, inicio_puerto, fin_puerto)
