---------------Escáner de Red y Puertos en Python---------------

Descripción
Este proyecto es un escáner de red y puertos desarrollado en Python que permite:

+ Detectar dispositivos activos en una red local mediante ping.

+ Identificar el sistema operativo de los dispositivos (basado en el valor del TTL).

+ Escanear un rango de puertos especificado para cada dispositivo encontrado.

+ Obtener banners de servicios abiertos en los puertos (cuando es posible).

+ El script utiliza programación concurrente para realizar múltiples tareas de escaneo en paralelo, logrando una exploración más rápida y eficiente.

---------------¿Cómo funciona?---------------
1) Ingreso de red y rango de puertos:
El usuario introduce una red en formato CIDR (por ejemplo, 192.168.1.0/24) y define el rango de puertos a escanear.

2) Detección de dispositivos activos:
Se envía un ping a cada dirección IP dentro de la red.
Si un dispositivo responde, se intenta identificar su sistema operativo basándose en el TTL.

3)Escaneo de puertos:
Para cada dispositivo activo, se escanean los puertos en el rango definido.
Si un puerto está abierto, el programa intenta capturar el banner del servicio para obtener más información.

4)Salida:
El script muestra:

 + IPs activas junto con su sistema operativo detectado.

 + Puertos abiertos y, si es posible, el banner del servicio asociado.

---------------Requisitos---------------
 + Python 3.6+

 + Librerías estándar de Python:
 (no requiere instalaciones adicionales)

---------------Uso---------------

1)Ejecutar el script:

 + bash: python escaner_red.py

2)Ingresar los datos cuando se solicite:
 + Red a escanear (ejemplo: 192.168.1.0/24).

 + Puerto inicial y final (ejemplo: 20 a 80).

Funciones principales
+ detectar_sistema_operativo(ip):
  Realiza un ping a la IP y determina el sistema operativo basándose en el TTL.

+ ping_dispositivo(ip):
  Pingea un dispositivo para verificar si está activo.

+ escanear_puerto(ip, puerto):
  Intenta conectar a un puerto específico y, si está abierto, captura el banner.

+ escanear_puertos(ip, inicio_puerto, fin_puerto):
  Escanea un rango de puertos de una IP usando múltiples hilos.

+ escanear_red(red, inicio_puerto, fin_puerto):
  Coordina la detección de dispositivos activos y el escaneo de sus puertos.

---------------Consideraciones---------------
+ Este script necesita permisos adecuados para enviar paquetes ICMP (ping).

+ El escaneo de puertos puede ser detectado por firewalls o sistemas de prevención de intrusiones (IDS).

+ Úsalo únicamente en redes donde tengas permiso explícito para escanear.

Licencia
Proyecto creado para fines educativos y de auditoría de seguridad.
Uso responsable recomendado.
