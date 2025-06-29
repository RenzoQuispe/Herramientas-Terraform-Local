provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_deployment" "app" {
    
  metadata {
    name = "nginx-deployment"
    labels = {
      app = "nginx-app-deployment"
    }
  }

  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "nginx-app"
      }
    }
    template {
      metadata {
        labels = {
          app = "nginx-app"
        }
      }
      spec {
        container {
          name  = "web-contenedor"
          image = "nginx:1.25"
          port {
            container_port = 80
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "app" {
  metadata {
    name = "miapp-service"
  }
  spec {
    selector = {
      app = "nginx-app"
    }
    port {
      port        = 80
      target_port = 80
    }
    type = "ClusterIP"
  }
}
