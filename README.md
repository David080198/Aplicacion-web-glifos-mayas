# 📜 Diccionario de Glifos Mayas

Sistema web para la consulta y clasificación de glifos mayas del Instituto Politécnico Nacional (IPN).

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-IPN-red)

## 📋 Descripción

Esta aplicación web permite a investigadores y estudiantes consultar un diccionario digital de glifos mayas, con funcionalidades de:

- 🔍 Búsqueda por número Thomson, traducción y transcripción
- 🏷️ Filtrado por atributos visuales
- 👤 Sistema de usuarios con registro y autenticación
- 🌐 Soporte para español e inglés
- 📱 Diseño responsivo (escritorio y móvil)

## 🏗️ Arquitectura

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Nginx     │────▶│   Flask     │────▶│   MySQL     │
│   (Puerto   │     │   App       │     │   8.0       │
│    81)      │     │  (Gunicorn) │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │ phpMyAdmin  │
                    │ (Puerto 82) │
                    └─────────────┘
```

## 🚀 Instalación y Ejecución

### Prerrequisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado
- Git (opcional)

### Pasos

1. **Clonar el repositorio** (o descargar el proyecto):
   ```bash
   git clone <url-del-repositorio>
   cd docker_compose_david_final_page_v2_nuevo_1
   ```

2. **Configurar variables de entorno**:
   
   Crear archivo `.env` en la raíz del proyecto (ya incluido con valores por defecto):
   ```env
   MYSQL_ROOT_PASSWORD=tu_password_seguro
   MYSQL_USER=root
   MYSQL_PASSWORD=tu_password_seguro
   SECRET_KEY=tu_clave_secreta_muy_larga
   # ... ver archivo .env para todas las variables
   ```

3. **Iniciar los servicios**:
   ```bash
   docker-compose up -d --build
   ```

4. **Acceder a la aplicación**:
   - 🌐 **Aplicación principal**: http://localhost:81
   - 🛠️ **phpMyAdmin**: http://localhost:82

### Comandos útiles

```bash
# Ver estado de los contenedores
docker-compose ps

# Ver logs de la aplicación
docker-compose logs app -f

# Detener todos los servicios
docker-compose down

# Reiniciar con datos limpios (⚠️ borra la BD)
docker-compose down -v
rm -rf db_data15/*
docker-compose up -d --build
```

## 📁 Estructura del Proyecto

```
├── app/
│   ├── Dockerfile          # Imagen Docker de la aplicación
│   ├── requirements.txt    # Dependencias Python
│   ├── wsgi.py            # Aplicación Flask principal
│   ├── static/
│   │   ├── css/           # Hojas de estilo
│   │   ├── js/            # Scripts JavaScript
│   │   └── imgs/          # Imágenes
│   └── templates/         # Plantillas HTML (Jinja2)
├── db/
│   └── init.sql           # Script de inicialización de BD
├── db_data15/             # Datos persistentes de MySQL
├── docker-compose.yml     # Configuración de servicios
├── nginx.conf             # Configuración de Nginx
├── .env                   # Variables de entorno (NO SUBIR A GIT)
├── .gitignore             # Archivos ignorados por Git
└── README.md              # Este archivo
```

## 🔧 Configuración

### Variables de Entorno (.env)

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `SECRET_KEY` | Clave secreta de Flask | (cambiar en producción) |
| `MYSQL_ROOT_PASSWORD` | Contraseña root de MySQL | - |
| `MYSQL_HOST` | Host de MySQL | `db` |
| `MYSQL_PORT` | Puerto de MySQL | `3306` |
| `MYSQL_DB` | Nombre de la base de datos | `base_grigori` |
| `MAIL_SERVER` | Servidor SMTP | `smtp.gmail.com` |
| `MAIL_PORT` | Puerto SMTP | `465` |
| `MAIL_USERNAME` | Email para envíos | - |
| `MAIL_PASSWORD` | Contraseña de aplicación | - |

### Puertos Expuestos

| Servicio | Puerto |
|----------|--------|
| Aplicación (Nginx) | 81 |
| phpMyAdmin | 82 |
| MySQL | 3308 |

## 🔒 Seguridad

### Mejoras implementadas

- ✅ **Consultas SQL parametrizadas** para prevenir SQL Injection
- ✅ **Variables de entorno** para credenciales sensibles
- ✅ **Logging sin información sensible**
- ✅ **Headers de seguridad** en Nginx (X-Frame-Options, X-Content-Type-Options, etc.)
- ✅ **Compresión gzip** habilitada
- ✅ **Healthchecks** en contenedores

### Recomendaciones para producción

1. **Cambiar todas las contraseñas** en el archivo `.env`
2. **No subir `.env`** al repositorio (está en `.gitignore`)
3. **Habilitar HTTPS** con certificados SSL
4. **Configurar firewall** para restringir acceso a puertos
5. **Implementar rate limiting** en Nginx
6. **Realizar backups regulares** de la base de datos

## 🗄️ Base de Datos

### Tablas principales

- `t_general` - Información general de glifos
- `t_attributes` - Atributos de glifos
- `t_distinction` - Relación glifos-atributos
- `register_users` - Usuarios registrados
- `atributos_guardados` - Atributos guardados por usuarios
- `atributos_personales` - Atributos personalizados

### Acceso a phpMyAdmin

1. Ir a http://localhost:82
2. Usuario: `root`
3. Contraseña: (la configurada en `.env`)

## 🐛 Solución de Problemas

### Error: "MySQL server host 'db' not found"
```bash
# Reiniciar los servicios
docker-compose down
docker-compose up -d
```

### Error: "Table doesn't exist"
```bash
# Reinicializar la base de datos
docker-compose down
rm -rf db_data15/*
docker-compose up -d
```

### La aplicación no responde
```bash
# Ver logs para diagnóstico
docker-compose logs app --tail 50
docker-compose logs db --tail 50
```

## 👥 Contribuidores

- Instituto Politécnico Nacional (IPN)
- Centro de Investigación en Computación (CIC)

## 📄 Licencia

Este proyecto es propiedad del Instituto Politécnico Nacional.

---

**Instituto Politécnico Nacional** - *"La Técnica al Servicio de la Patria"*
