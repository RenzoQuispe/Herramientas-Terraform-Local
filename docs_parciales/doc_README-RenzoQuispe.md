## Coautor README: Quispe Villena

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