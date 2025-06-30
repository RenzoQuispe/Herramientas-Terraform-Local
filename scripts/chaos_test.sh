#!/bin/bash

echo "chaos testing minimal"

deployment="nginx-deployment"
imagen="web-contenedor"
service="miapp-service"

# verificamos que el deployment y service existen (terraform init y terraform apply)
kubectl get deployment $deployment > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Deployment '$deployment' no encontrado, ejecuta terraform apply"
  exit 1
fi

kubectl get service $service > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Service '$service' no encontrado, ejecuta terraform apply"
  exit 1
fi

# simulamos un drift en el cluster kubernetes
echo "- Escalando Deployment para inducir drift en replicas"
kubectl scale deployment "$deployment" --replicas=5

echo "- Cambiando imagen del contenedor para inducir drift en la imagen"
kubectl set image deployment/"$deployment" "$imagen"=nginx:2.0

echo "- Cambiando tipo del Service para inducir drift en el tipo"
kubectl patch service "$service" -p '{"spec": {"type": "NodePort"}}'

#Comparamos con el estado deseado
echo "- Ejecutando comparador para verificar drift:"
python3 scripts/state_comparador.py
salida=$?
if [ $salida -eq 1 ]; then
  echo "Drift detectado correctamente"
else
  echo "No se detectó drift cuando se esperaba"
fi

# regresamos al estado deseado
echo "Restaurando al estado deseado definido en iac/main.tf"
terraform -chdir=iac/ apply -auto-approve

echo "Estado restaurado, chaos test finalizado"