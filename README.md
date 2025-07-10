# Herramientas para Gestión, Detección de Drift y Recuperación en Infraestructura Local con Terraform

## Descripción de archivos

`backup_state.sh`
- Crea una carpeta `backups/`, si no existe, para almacenar todos los archivos de respaldo.
- Se genera el nombre del backup añadiendo un timestamp, con formato `YYYY-MM-DD_HH-MM-SS`, al final.
- Se inserta el estado actual (en el momento de la ejecución del script) del archivo de estado de terraform `terraform.tfstate`. 

`restore_state.sh`
- Lee todos los archivos de respaldo en la carpeta `backups/` y verifica que haya al menos un archivo.
- Muestra una lista de los archivos de respaldo y le pide al usuario escribir el número correspondiente al backup que quiere restaurar.
- Copia el archivo de respaldo a la ruta de `terraform.tfstate` (en `iac/`) y restaura el estado.

`chaos_test.sh`
- Simula un Chaos Testing minimal para un clúster Kubernetes, induciendo cambios intencionales en recursos clave
para verificar que las desviaciones se detecten correctamente con state_comparador.py.

`state_comparador.py`
- Lee el archivo con la infraestructura deseada `terraform.tfstate`.
- Obtiene el estado real de la infraestructura con `kubectl get -o json`.
- Compara los estados y detecta si hay drift o no.
- Imprime una tabla ASCII con la comparación.

`main.tf`
- Minikube corre un cluster local de Kubernetes
- El Deployment nginx-deployment crea 2 pods  con contenedores docker nginx:1.25 expuestos en el puerto 80 
- El Service miapp-service de tipo ClusterIP expone internamente los pods y balancea trafico entre ellos

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

## Requisitos técnicos
```
| Herramientas | Versión       |
|   Python     | >= 3.10       |
|    Bash      | >= 5.1.16     |
|   minikube   | >= 1.36.0     |
|  terraform   | >= 1.6.3      |
|   kubectl    | >= 1.33       |
|     jq       | >= 1.6        |
|    rsync     | >= 3.1.0      |
```
## Funcionamiento de la infraestructura definida en iac/main.tf
```markdown
git clone https://github.com/RenzoQuispe/Herramientas-Terraform-Local.git
cd Herramientas-Terraform-Local
# iniciar terraform
cd iac
terraform init
terraform apply
# verificar el estado de los recursos creados por terraform
kubectl get deployments
kubectl get pods
kubectl get svc
```

## Funcionamiento de la scripts
1. `backup_state.sh` y `restore_state.sh`

    ```markdown
    # Primero tener iniciado terraform en iac/
    # Dar permisos de ejecucion a los scripts
    chmod +x scripts/backup_state.sh
    chmod +x scripts/restore_state.sh
    # probar scripts con:   
    ./scripts/backup_state.sh
    ./scripts/restore_state.sh
    ```
      Con el script backup_state.sh podemos crear multiples backup de terraform.state, y luego con restore_state.sh podemos listarlos y restaurar terraform.tfstate a un estado anterior.

2. `state_comparador.py`
    Primero tener en funcionamiento la infraestructura definida en iac/main.tf (Seccion anterior)
    ```
    cd scripts
    python state_comparador.py
    ```

## Diagramas del proceso de backup/restauración

1. Creación de backup con backup_state.sh
    ```
    [terraform.tfstate] 
          |
          v
    [backup_state.sh] --->  Se crea copia incremental con rsync
                            /backups/tfstate_2025-06-20_18-30-00.backup/terraform.tfstate

    Estructura del backup:
    /backups/
    └── tfstate_2025-06-20_18-30-00.backup/
          └── terraform.tfstate  (copia nueva o hardlink a copia anterior)
    ```
2. Simulación de desastre
    ```
    Usuario borra o modifica terraform.state

    Estado:
    [terraform.tfstate] -->  no existe o esta dañado
    ```
3. Restauración con restore_state.sh
    ```
    [restore_state.sh] ---> Lista backups disponibles
          |
          v
    se selecciona un backup a traves de un menu: tfstate_2025-06-20_18-30-00.backup
          |
          v
    Verifica validez JSON (jq)
          |
          v
    Copia archivo de backup al directorio original

    Resultado:
    [terraform.tfstate] --> restaurado a un estado anterior
    ```

## Ejecucion de pruebas y cobertura
### Pruebas unitarias
```markdown
git clone https://github.com/RenzoQuispe/Herramientas-Terraform-Local.git
cd Herramientas-Terraform-Local
python3 -m venv venv
source venv/bin/activate
pip install pytest pytest-cov prettytable
pytest --cov=scripts -v
```
### Chaos testing minimal
```markdown
git clone https://github.com/RenzoQuispe/Herramientas-Terraform-Local.git
cd Herramientas-Terraform-Local
# tener creado los recursos
cd iac
terraform init
terraform apply
# chaos testing minimal
cd ..
chmod +x scripts/chaos_test.sh
./scripts/chaos_test.sh 
```