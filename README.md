## Proyecto 7 - Operaciones y recuperación ante desastres locales para infraestructura Terraform

Quispe Villena Renzo - renzo.quispe.v@uni.pe

URL del repositorio grupal: https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4

### Aportes al proyecto
#### Sprint 1
Defini una infraestructura deseada el cual sera usado para hacer simulaciones de drift para desarrollar la herramienta de deteccion de drift. Para probar la creacion de recursos de infraestructura definida con terraform en main.tf se usa un cluster de kubernetes local con minikube.

```
                    Minikube
                       |
                       |
            ---------------------------
            Deployment: nginx-deployment
              Replicas: 2 Pods
            ---------------------------
                       |
                       |
          --------------------       --------------------
          Pod: nginx-app-1           Pod: nginx-app-2
          Container:                 Container:
            web-contenedor             web-contenedor
          Image: nginx:1.25          Image: nginx:1.25
          Port: 80                   Port: 80
          --------------------       --------------------
                       |                    |
                       |                    |
                       --------+-------------
                               |
                               |
                       --------------------
                       Service: miapp-service
                       Type: ClusterIP
                       Port: 80
                       --------------------

```
- Minikube corre un cluster local de Kubernetes
- El Deployment nginx-deployment crea 2 pods  con contenedores docker nginx:1.25 expuestos en el puerto 80 
- El Service miapp-service de tipo ClusterIP expone internamente los pods y balancea trafico entre ellos

#### Sprint 2
Implemente pruebas unitarias en tests/test_state_comparador.py para la logica de comparacion de estado y las funciones dentro de state_comparador.py, se aplicaron principios SOLID a los tests.

#### Sprint 3
Implemente el script chaos_test.sh que simula un Chaos Testing minimal para un clúster Kubernetes, induciendo cambios intencionales en recursos clave para verificar que las desviaciones se detecten correctamente con state_comparador.py. A diferencia de las pruebas unitarias con pytest, que validan la correcta funcionalidad de fragmentos de codigo aislados, este script prueba la resiliencia de la herramienta en una simulacion de despligue real, asegurando que la infraestructura se mantenga alineada con su configuracion declarada con terraform.

### Requisitos técnicos
```
| Herramientas | Versión       |
|   minikube   | >= 1.36.0     |
|  terraform   | >= 1.6.3      |
|   kubectl    | >= 1.33       |
```
### Funcionamiento de la infraestructura definida en iac/main.tf
```markdown
git clone https://github.com/RenzoQuispe/Proyecto-9-Personal.git
cd Proyecto-9-Personal
# iniciar terraform
cd iac
terraform init
terraform apply
# verificar el estado de los recursos creados por terraform
kubectl get deployments
kubectl get pods
kubectl get svc
```
### Ejecucion de pruebas y cobertura
#### Pruebas unitarias
```markdown
git clone https://github.com/RenzoQuispe/Proyecto-9-Personal.git
cd Proyecto-9-Personal
python3 -m venv venv
source venv/bin/activate
pip install pytest pytest-cov prettytable
pytest --cov=scripts -v
```
#### Chaos testing minimal
```markdown
git clone https://github.com/RenzoQuispe/Proyecto-9-Personal.git
cd Proyecto-9-Personal
# tener creado los recursos
cd iac
terraform init
terraform apply
# chaos testing minimal
cd ..
chmod +x scripts/chaos_test.sh
./scripts/chaos_test.sh 
```