job "getlock" {
  datacenters = ["agrrh"]

  priority = 80

  group "storage" {
    count = 1

    affinity {
      attribute = "${meta.class}"
      value     = "storage"
      weight    = 100
    }

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
          "local/redis.conf:/usr/local/etc/redis/redis.conf",
        ]

        command = "redis-server"
        args = [
          "/usr/local/etc/redis/redis.conf"
        ]

        ports = ["redis"]
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
      }
    }

    network {
      port "redis" { to = 6379 }
    }
  }

  group "api-v1" {
    count = 2

    affinity {
      attribute = "${meta.class}"
      value     = "compute"
      weight    = 100
    }

    spread {
      attribute = "${node.unique.name}"
    }

    task "getlock" {
      driver = "docker"

      leader = true

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
        image = "agrrh/getlock:v0.3.0"

        volumes = [
          "local/config.yml:/app/config.yml"
        ]

        ports = ["api"]
      }

      kill_signal = "SIGTERM"

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
          "traefik.http.routers.http-getlock-tech-api-v1.entrypoints=http",
          "traefik.http.routers.http-getlock-tech-api-v1.rule=Host(\"getlock.tech\") && PathPrefix(\"/v1/\")",
          "traefik.http.routers.http-getlock-tech-api-v1.middlewares=redir-https,strip-v1",
          # https
          "traefik.http.routers.https-getlock-tech-api-v1.entrypoints=https",
          "traefik.http.routers.https-getlock-tech-api-v1.rule=Host(\"getlock.tech\") && PathPrefix(\"/v1/\")",
          "traefik.http.routers.https-getlock-tech-api-v1.middlewares=strip-v1",
          "traefik.http.routers.https-getlock-tech-api-v1.tls=true",
          "traefik.http.routers.https-getlock-tech-api-v1.tls.certresolver=http",
        ]
      }

      resources {
        cpu    = 100
        memory = 64
      }

      logs {
        max_files     = 2
        max_file_size = 50
      }
    }

    network {
      port "api" { to = 8000 }
    }
  }

  group "api-v2" {
    count = 3

    affinity {
      attribute = "${meta.class}"
      value     = "compute"
      weight    = 100
    }

    spread {
      attribute = "${node.unique.name}"
    }

    task "getlock" {
      driver = "docker"

      leader = true

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
  db: 1
  password: null
{{ end }}
EOF

        destination   = "local/config.yml"
      }

      config {
        force_pull = true
        image = "agrrh/getlock:v1.0.1"

        volumes = [
          "local/config.yml:/app/config.yml"
        ]

        ports = ["api"]
      }

      kill_signal = "SIGTERM"

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
          "traefik.http.middlewares.strip-v2.stripprefix.prefixes=/v2",
          # http
          "traefik.http.routers.http-getlock-tech-api-v2.entrypoints=http",
          "traefik.http.routers.http-getlock-tech-api-v2.rule=Host(\"getlock.tech\") && PathPrefix(\"/v2/\")",
          "traefik.http.routers.http-getlock-tech-api-v2.middlewares=redir-https,strip-v2",
          # https
          "traefik.http.routers.https-getlock-tech-api-v2.entrypoints=https",
          "traefik.http.routers.https-getlock-tech-api-v2.rule=Host(\"getlock.tech\") && PathPrefix(\"/v2/\")",
          "traefik.http.routers.https-getlock-tech-api-v2.middlewares=strip-v2",
          "traefik.http.routers.https-getlock-tech-api-v2.tls=true",
          "traefik.http.routers.https-getlock-tech-api-v2.tls.certresolver=http",
        ]
      }

      resources {
        cpu    = 100
        memory = 64
      }

      logs {
        max_files     = 2
        max_file_size = 50
      }
    }

    network {
      port "api" { to = 8000 }
    }
  }

  group "front" {
    count = 2

    affinity {
      attribute = "${meta.class}"
      value     = "web"
      weight    = 100
    }

    spread {
      attribute = "${node.unique.name}"
    }

    task "nginx" {
      driver = "docker"

      config {
        force_pull = true
        image = "agrrh/getlock-front:dev"

        ports = ["http"]
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
          "traefik.http.routers.http-app-getlock-tech.entrypoints=http",
          "traefik.http.routers.http-app-getlock-tech.rule=Host(\"app.getlock.tech\")",
          "traefik.http.routers.http-app-getlock-tech.middlewares=redir-https",
          # https
          "traefik.http.routers.https-app-getlock-tech.entrypoints=https",
          "traefik.http.routers.https-app-getlock-tech.rule=Host(\"app.getlock.tech\")",
          "traefik.http.routers.https-app-getlock-tech.tls=true",
          "traefik.http.routers.https-app-getlock-tech.tls.certresolver=http",
        ]
      }

      resources {
        cpu    = 100
        memory = 32
      }

      logs {
        max_files     = 2
        max_file_size = 10
      }
    }

    network {
      port "http" { to = 80 }
    }
  }

  group "docs" {
    count = 2

    affinity {
      attribute = "${meta.class}"
      value     = "web"
      weight    = 100
    }

    spread {
      attribute = "${node.unique.name}"
    }

    task "nginx" {
      driver = "docker"

      config {
        force_pull = true
        image = "agrrh/getlock-docs:v0.3.0"

        ports = ["http"]
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
      }

      logs {
        max_files     = 2
        max_file_size = 10
      }
    }

    network {
      port "http" { to = 80 }
    }
  }
}
