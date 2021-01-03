job "getlock" {
  datacenters = ["agrrh"]

  priority = 80

  group "storage" {
    count = 1

    ephemeral_disk {
      sticky = true
      migrate = true
      size = 300
    }

    task "redis" {
      driver = "docker"

      template {
        data = <<EOF
appendonly yes

# NOTE Consider using "save 10x x" formula as each /health call leads to write-read-delete operations
save 30 6
EOF

        destination   = "local/redis.conf"
      }

      config {
        force_pull = true
        image = "redis:5.0.10"

        volumes = [
          "local/redis.conf:/usr/local/etc/redis/redis.conf"
        ]

        command = "redis-server"
        args = [
          "/usr/local/etc/redis/redis.conf"
        ]

        port_map {
          redis = 6379
        }
      }

      service {
        name = "getlock-storage-redis"

        check {
          type     = "tcp"
          port     = "redis"
          interval = "10s"
          timeout  = "2s"
        }

        port = "redis"
      }

      resources {
        cpu    = 200
        memory = 256
        network {
          mbits = 10
          port "redis" {}
        }
      }
    }
  }

  group "api" {
    count = 3

    spread {
      attribute = "${node.unique.name}"
    }

    update {
      max_parallel = 1
    }

    ephemeral_disk {
      sticky = true
      migrate = true
      size = 200
    }

    task "getlock" {
      driver = "docker"

      env {
        CONFIG_PATH = "./config.yml"
      }

      template {
        data = <<EOF
---

flask:
  debug: false
  threaded: true
  host: 0.0.0.0
  port: 8000

{{ range service "getlock-storage-redis" }}
redis:
  host: {{ .Address }}
  port: {{ .Port }}
  db: 0
  password: null
{{ end }}
EOF

        destination   = "local/config.yml"
      }

      config {
        force_pull = true
        image = "agrrh/getlock:v0.2.0"

        volumes = [
          "local/config.yml:/app/config.yml"
        ]

        port_map {
          api = 8000
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
          "traefik.http.routers.http-getlock-tech-api.rule=Host(\"getlock.tech\") && PathPrefix(\"/v1/\")",
          "traefik.http.routers.http-getlock-tech-api.middlewares=redir-https,strip-v1",
          # https
          "traefik.http.routers.https-getlock-tech-api.entrypoints=https",
          "traefik.http.routers.https-getlock-tech-api.rule=Host(\"getlock.tech\") && PathPrefix(\"/v1/\")",
          "traefik.http.routers.https-getlock-tech-api.middlewares=strip-v1",
          "traefik.http.routers.https-getlock-tech-api.tls=true",
          "traefik.http.routers.https-getlock-tech-api.tls.certresolver=http",
        ]
      }

      resources {
        cpu    = 100
        memory = 64
        network {
          mbits = 10
          port "api" {}
        }
      }

      logs {
        max_files     = 2
        max_file_size = 50
      }
    }
  }

  group "docs" {
    count = 2

    spread {
      attribute = "${node.unique.name}"
    }

    update {
      max_parallel = 1
    }

    ephemeral_disk {
      sticky = true
      migrate = true
      size = 100
    }

    task "nginx" {
      driver = "docker"

      config {
        force_pull = true
        image = "agrrh/getlock-docs:v0.2.0"

        port_map {
          http = 80
        }
      }

      service {
        check {
          type     = "http"
          port     = "http"
          path     = "/"
          interval = "10s"
          timeout  = "1s"
        }

        port = "http"

        tags = [
          "traefik.enable=true",
          # middlewares
          "traefik.http.middlewares.redir-https.redirectscheme.scheme=https",
          # http
          "traefik.http.routers.http-getlock-tech-docs.entrypoints=http",
          "traefik.http.routers.http-getlock-tech-docs.rule=Host(\"getlock.tech\")",
          "traefik.http.routers.http-getlock-tech-docs.middlewares=redir-https",
          # https
          "traefik.http.routers.https-getlock-tech-docs.entrypoints=https",
          "traefik.http.routers.https-getlock-tech-docs.rule=Host(\"getlock.tech\")",
          "traefik.http.routers.https-getlock-tech-docs.tls=true",
          "traefik.http.routers.https-getlock-tech-docs.tls.certresolver=http",
        ]
      }

      resources {
        cpu    = 100
        memory = 32
        network {
          mbits = 10
          port "http" {}
        }
      }

      logs {
        max_files     = 2
        max_file_size = 10
      }
    }
  }
}
