job "getlock" {
  datacenters = ["agrrh"]

  priority = 80

  constraint {
    distinct_hosts = "true"
  }

  update {
    max_parallel = 1
  }

  group "api" {
    count = 1

    task "getlock" {
      driver = "docker"

      env {
        CONFIG_PATH = "./config.example.yml"
      }

      config {
        force_pull = true
        image = "agrrh/getlock:v0.1.0"

        port_map {
          http = 5000
        }
      }

      service {
        check {
          type     = "http"
          port     = "api"
          path     = "/health"
          interval = "10s"
          timeout  = "1s"
        }

        port = "api"

        tags = [
          "traefik.enable=true",
          # middlewares
          "traefik.http.middlewares.redir-https.redirectscheme.scheme=https",
          "traefik.http.middlewares.strip-v1.stripprefix.prefixes=/v1",
          # http
          "traefik.http.routers.http-getlock-tech-api.entrypoints=http",
          "traefik.http.routers.http-getlock-tech-api.rule=Host(\"getlock.tech\") && PathPrefix(\"/v1\")",
          "traefik.http.routers.http-getlock-tech-api.middlewares=redir-https,strip-v1",
          # https
          "traefik.http.routers.https-getlock-tech-api.entrypoints=https",
          "traefik.http.routers.https-getlock-tech-api.rule=Host(\"getlock.tech\") && PathPrefix(\"/v1\")",
          "traefik.http.routers.https-getlock-tech-api.middlewares=strip-v1",
          "traefik.http.routers.https-getlock-tech-api.tls=true",
          "traefik.http.routers.https-getlock-tech-api.tls.certresolver=http",
        ]
      }

      resources {
        cpu    = 128
        memory = 128
        network {
          mbits = 10
          port "api" {}
        }
      }

      logs {
        max_files     = 2
        max_file_size = 100
      }
    }
  }
}
