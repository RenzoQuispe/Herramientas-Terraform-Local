# Contribuciones de Renzo Quispe Villena

## Sprint 1
- 2025-06-22: Escribí `iac/main.tf` que define una infraestructura local en Kubernetes usando Terraform para pruebas locales con Minikube.Se crea un Deployment con 2 réplicas del contenedor nginx:1.25 y un Service de tipo ClusterIP, que permite conectar internamente y balancear tráfico entre esos pods.
Commit: [`feat(tf): (issue #1) agregar iac/main.tf con infraestructura local`](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/pull/5/commits/f107a5b99c1eb5942db9aaaeff1270019f548b85).
Pull request grupal: [#5](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/pull/5)

- 2025-06-22: Se actualizaron los nombres-labels en iacmain.tf por unos nombres mas descriptivos .  
Commit: [`refactor(tf): actualizar nombres genericos "miapp" en iac/main.tf con`](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/pull/5/commits/7328df6f62ad72635b1c04d44f74d424bb91d622). 
Pull request grupal: [#5](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/pull/5)

## Sprint 2
- 2025-06-29: Escribí `tests/test_state_comparador.py` con pruebas unitarias para la logica de comparador en `scripts/state_comparador.py`.
Commit: [`test(py): agregar pruebas unitarias para la lógica de comparación de estado de state_comparador.py`](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/pull/20/commits/3fa63894b0dfb2fe70713c79f7c462c107500f25).
Pull request grupal: [#20](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/pull/20)

- 2025-06-29: Actualize `tests/test_state_comparador.py` con mas pruebas unitarias para el resto de funciones de `scripts/state_comparador.py`: cargar_tfstate, obtener_estado_deseado, y obtener_estado_real.
Commit: [`test(py): actualizar test_ state_comparador.py con test de las funciones cargar_tfstate, obtener_estado_deseado, y obtener_estado_real`](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/pull/20/commits/0adfbf67078cf2668baf20dce2d8b1b141a7c97e). 
Pull request grupal: [#20](https://github.com/Grupo-9-CC3S2/Proyecto-9-PC4/pull/20)

