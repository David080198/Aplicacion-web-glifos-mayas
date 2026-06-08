# Guía de Despliegue en Dokploy

## 📦 Requisitos Previos

- Cuenta en Dokploy
- Repositorio Git con el código
- Variables de entorno configuradas

## 🚀 Pasos para Desplegar

### 1. Preparar Variables de Entorno

En Dokploy, configura las siguientes variables de entorno:

```bash
SECRET_KEY=tu-clave-secreta-aqui
MYSQL_ROOT_PASSWORD=tu-password-mysql
MYSQL_USER=root
MYSQL_PASSWORD=tu-password-mysql
MYSQL_DB=base_grigori
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-app-password
MAIL_USE_TLS=True
MAIL_USE_SSL=False
```

### 2. Conectar Repositorio

1. Ve a tu panel de Dokploy
2. Crea un nuevo proyecto
3. Selecciona "Docker Compose"
4. Conecta tu repositorio Git
5. Selecciona la rama principal

### 3. Configurar Build

- **Build Context**: `.`
- **Docker Compose File**: `docker-compose.prod.yml`
- **Port**: `80`

### 4. Configurar Dominio

En la sección de dominios, añade:

- Tu dominio personalizado o usa el subdominio de Dokploy
- El puerto debe ser `80`

### 5. Desplegar

Haz clic en "Deploy" y espera a que el proceso termine.

## 🔄 Actualizaciones

Para actualizar la aplicación:

1. Haz push de tus cambios al repositorio
2. En Dokploy, haz clic en "Redeploy"
3. La aplicación se actualizará automáticamente

## 📊 Monitoreo

Dokploy proporciona:

- Logs en tiempo real
- Uso de recursos (CPU, RAM)
- Health checks automáticos

## 🐛 Troubleshooting

Si hay problemas:

1. Revisa los logs en Dokploy
2. Verifica las variables de entorno
3. Asegúrate de que el archivo `.env` esté configurado correctamente
4. Verifica que los puertos estén correctos

## 📝 Notas Importantes

- La base de datos se inicializará automáticamente con el archivo `init.sql`
- Los datos se persisten en un volumen de Docker
- El servidor Nginx actúa como proxy reverso
- Las contraseñas se almacenan con bcrypt (seguro)
