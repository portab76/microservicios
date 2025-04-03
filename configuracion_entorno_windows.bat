# PowerShell
# 1. Configuración Inicial en Windows 10

# 1.1. Habilitar Hyper-V (requiere reinicio)
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All

# 1.2. Instalar Docker Desktop
# Descargar desde: https://www.docker.com/products/docker-desktop
# Habilitar WSL2 backend en configuración

# 1.3. Instalar Windows Subsystem for Linux (WSL2)
wsl --install
wsl --set-default-version 2

# 1.4. Instalar Minikube para Windows
choco install minikube -y # Usando Chocolatey
# o descargar manualmente desde https://minikube.sigs.k8s.io/docs/start/

# 1.5. Instalar kubectl
choco install kubernetes-cli -y

# 1.6. Instalar Helm
choco install kubernetes-helm -y

# 2. Iniciar Minikube en Windows

# 2.1 Iniciar Minikube con el driver de Docker (requiere Docker Desktop corriendo)
 minikube start --driver=docker --memory=4096 --cpus=2

# 2.2 Verificar estado
minikube status

# 2.3 Configurar el contexto de kubectl

# 3. Instalar Kafka en Minikube (Windows)

# 3.1 # Añadir repositorio Helm
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# 3.1.1 Si no tienes helm instalado: Instalar Chocolatey si no lo tienes
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 3.1.2 Instalar Helm
choco install kubernetes-helm -y

3.2 # Instalar Kafka (igual que en Linux)
helm install kafka bitnami/kafka

3.3 # Verificar instalación
kubectl get pods -w