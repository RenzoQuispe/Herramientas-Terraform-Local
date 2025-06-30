import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.state_comparador import comparar, cargar_tfstate, obtener_estado_deseado, obtener_estado_real, NOMBRE_DEPLOYMENT, NOMBRE_SERVICE
import json
import pytest
from unittest.mock import patch, Mock
# tests para "comparar" de state_comparador
@pytest.mark.parametrize(
    "estado_deseado, estado_real, resultado_drift_esperado",
    [
        # caso sin drift
        (
            {
                "deployment": {
                    "replicas": 3,
                    "image": "nginx:1.25",
                    "container_port": 80,
                    "container_name": "web-contenedor"
                },
                "service": {
                    "port": 80,
                    "target_port": 80,
                    "type": "ClusterIP"
                }
            },
            {
                "deployment": {
                    "replicas": 3,
                    "image": "nginx:1.25",
                    "container_port": 80,
                    "container_name": "web-contenedor"
                },
                "service": {
                    "port": 80,
                    "target_port": 80,
                    "type": "ClusterIP"
                }
            },
            False
        ),

        # drift solo en replicas
        (
            {
                "deployment": {
                    "replicas": 4,
                    "image": "nginx:1.25",
                    "container_port": 80,
                    "container_name": "web-contenedor"
                },
                "service": {
                    "port": 80,
                    "target_port": 80,
                    "type": "ClusterIP"
                }
            },
            {
                "deployment": {
                    "replicas": 3,
                    "image": "nginx:1.25",
                    "container_port": 80,
                    "container_name": "web-contenedor"
                },
                "service": {
                    "port": 80,
                    "target_port": 80,
                    "type": "ClusterIP"
                }
            },
            True
        ),

        # drift en service port
        (
            {
                "deployment": {
                    "replicas": 3,
                    "image": "nginx:1.25",
                    "container_port": 80,
                    "container_name": "web-contenedor"
                },
                "service": {
                    "port": 8080,
                    "target_port": 80,
                    "type": "ClusterIP"
                }
            },
            {
                "deployment": {
                    "replicas": 3,
                    "image": "nginx:1.25",
                    "container_port": 80,
                    "container_name": "web-contenedor"
                },
                "service": {
                    "port": 80,
                    "target_port": 80,
                    "type": "ClusterIP"
                }
            },
            True
        ),

        # drift en varios atributos
        (
            {
                "deployment": {
                    "replicas": 5,
                    "image": "nginx:1.26",
                    "container_port": 8080,
                    "container_name": "web-contenedor-2"
                },
                "service": {
                    "port": 8080,
                    "target_port": 8080,
                    "type": "LoadBalancer"
                }
            },
            {
                "deployment": {
                    "replicas": 3,
                    "image": "nginx:1.25",
                    "container_port": 80,
                    "container_name": "web-contenedor"
                },
                "service": {
                    "port": 80,
                    "target_port": 80,
                    "type": "ClusterIP"
                }
            },
            True
        )
    ]
)
def test_comparar(estado_deseado, estado_real, resultado_drift_esperado):
    drift = comparar(estado_deseado, estado_real)
    assert drift == resultado_drift_esperado
    
# tests para "cargar_tfstate"
def test_cargar_tfstate(tmp_path):
    contenido = {
        "version": 4,
        "terraform_version": "1.6.3",
        "serial": 45,
        "lineage": "4555872b-7f57-ed73-f8c0-8b25d19915d6",
        "outputs": {},
        "resources": [],
        "check_results": {}
    }
    archivo = tmp_path / "terraform.tfstate"
    archivo.write_text(json.dumps(contenido))
    estado = cargar_tfstate(str(archivo))
    assert estado == contenido
def test_cargar_tfstate_error():
    with pytest.raises(IOError):
        cargar_tfstate("no_existe.tfstate")
# tests para "obtener_estado_deseado"
def test_obtener_estado_deseado():
    tfstate = {
        "resources": [
            {
                "type": "kubernetes_deployment",
                "instances": [
                    {
                        "attributes": {
                            "spec": [
                                {
                                    "replicas": 3,
                                    "template": [
                                        {
                                            "spec": [
                                                {
                                                    "container": [
                                                        {
                                                            "image": "nginx:1.25",
                                                            "port": [{"container_port": 80}],
                                                            "name": "web-contenedor"
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "metadata": [{"name": "nginx-deployment"}]
                        }
                    }
                ]
            },
            {
                "type": "kubernetes_service",
                "instances": [
                    {
                        "attributes": {
                            "spec": [
                                {
                                    "port": [{"port": 80, "target_port": 80}],
                                    "type": "ClusterIP"
                                }
                            ],
                            "metadata": [{"name": "miapp-service"}]
                        }
                    }
                ]
            }
        ]
    }
    estado = obtener_estado_deseado(tfstate)
    assert estado["deployment"]["replicas"] == 3
    assert estado["deployment"]["image"] == "nginx:1.25"
    assert estado["deployment"]["container_port"] == 80
    assert estado["deployment"]["container_name"] == "web-contenedor"
    assert estado["service"]["port"] == 80
    assert estado["service"]["target_port"] == 80
    assert estado["service"]["type"] == "ClusterIP"

# test para "obtener_estado_real"
@patch("scripts.state_comparador.subprocess.run")
def test_obtener_estado_real(mock_test):
    global NOMBRE_DEPLOYMENT, NOMBRE_SERVICE
    NOMBRE_DEPLOYMENT = "nginx-deployment"
    NOMBRE_SERVICE = "miapp-service"

    deploy_mock = {
        "spec": {
            "replicas": 3,
            "template": {
                "spec": {
                    "containers": [
                        {
                            "image": "nginx:1.25",
                            "ports": [{"containerPort": 80}],
                            "name": "web-contenedor"
                        }
                    ]
                }
            }
        }
    }

    service_mock = {
        "spec": {
            "ports": [{"port": 80, "targetPort": 80}],
            "type": "ClusterIP"
        }
    }

    # mock kubectl get deployment
    mock_test.side_effect = [
        Mock(stdout=json.dumps(deploy_mock)),
        Mock(stdout=json.dumps(service_mock))
    ]

    estado = obtener_estado_real()
    assert estado["deployment"]["replicas"] == 3
    assert estado["deployment"]["image"] == "nginx:1.25"
    assert estado["deployment"]["container_port"] == 80
    assert estado["deployment"]["container_name"] == "web-contenedor"

    assert estado["service"]["port"] == 80
    assert estado["service"]["target_port"] == 80
    assert estado["service"]["type"] == "ClusterIP"
