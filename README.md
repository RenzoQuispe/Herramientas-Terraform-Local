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
