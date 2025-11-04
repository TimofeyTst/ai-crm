# Nginx Reverse Proxy - Production-Ready

---

## 🔥 NGINX КОНФИГ (PRODUCTION-READY)

### 1. ОСНОВНОЙ КОНФИГ: ci/nginx.conf

## 💻 УСТАНОВКА NGINX НА VM

### Шаг 1: Подключись к VM

```bash
ssh -i ~/.ssh/yc-key ubuntu@EXTERNAL_IP
```

### Шаг 2: Обнови систему

```bash
sudo apt update && sudo apt upgrade -y
```

### Шаг 3: Установи Nginx

```bash
sudo apt install -y nginx curl certbot python3-certbot-nginx
```

### Шаг 4: Скачай мой конфиг

```bash
# Сохрани nginx.conf (из выше) в /etc/nginx/nginx.conf
sudo nano /etc/nginx/nginx.conf

# ИЛИ скачай с GitHub/Gist
curl https://raw.githubusercontent.com/your-repo/nginx.conf \
  | sudo tee /etc/nginx/nginx.conf

# Проверь синтаксис
sudo nginx -t
```

### Шаг 5: Установи Let's Encrypt сертификат

```bash
# Останови Nginx временно (для certbot)
sudo systemctl stop nginx

# Получи сертификат
sudo certbot certonly --standalone \
  -d resume.pro \
  -d www.resume.pro \
  --email your-email@example.com \
  --agree-tos \
  --non-interactive

# Запусти Nginx обратно
sudo systemctl start nginx
```

### Шаг 6: Обнови конфиг с путями сертификатов

```bash
sudo nano /etc/nginx/nginx.conf

# Найди и обнови:
# ssl_certificate /etc/letsencrypt/live/resume.pro/fullchain.pem;
# ssl_certificate_key /etc/letsencrypt/live/resume.pro/privkey.pem;
```

### Шаг 7: Запусти Nginx

```bash
# Проверь конфиг
sudo nginx -t

# Запусти
sudo systemctl start nginx
sudo systemctl enable nginx  # Auto-start on reboot

# Проверь статус
sudo systemctl status nginx
```

---

## 🔄 АВТООБНОВЛЕНИЕ СЕРТИФИКАТОВ

```bash
# Cron job для автообновления
sudo crontab -e

# Добавь:
0 2 * * * /usr/bin/certbot renew --quiet --no-self-upgrade && systemctl reload nginx

# Сохрани (Ctrl+X, Y, Enter)
```

---

## 🐳 АЛЬТЕРНАТИВА: DOCKER + DOCKER-COMPOSE

### Запуск:

```bash
# На VM
docker-compose up -d

# Проверка
docker ps
docker logs nginx
```

---

## 📊 МОНИТОРИНГ

### Посмотри логи

```bash
# Real-time
sudo tail -f /var/log/nginx/resume_pro_access.log
sudo tail -f /var/log/nginx/resume_pro_error.log

# Посчитай requests
sudo wc -l /var/log/nginx/resume_pro_access.log

# Посмотри top IPs
sudo awk '{print $1}' /var/log/nginx/resume_pro_access.log | sort | uniq -c | sort -rn | head -10
```

### Проверь статус Nginx

```bash
sudo systemctl status nginx
ps aux | grep nginx
sudo netstat -tlnp | grep :443
```

### Проверь SSL сертификат

```bash
sudo openssl x509 -in /etc/letsencrypt/live/resume.pro/fullchain.pem -text -noout
echo | openssl s_client -servername resume.pro -connect 127.0.0.1:443
```

---

## 🔒 SECURITY CHECKS

### Проверь SSL рейтинг

```bash
# Перейди на https://www.ssllabs.com/ssltest/
# Введи свой домен
# Должен получить A+ rating
```

### Проверь security headers

```bash
curl -I https://resume.pro

# Должны быть:
# Strict-Transport-Security
# X-Frame-Options
# X-Content-Type-Options
# Content-Security-Policy
```

### Проверь DDoS защиту

```bash
# Rate limiting уже в конфиге
# Макс 10 req/sec на IP (zona: general)
# Макс 100 req/min на /api (zona: api)
```

---

## 🚨 TROUBLESHOOTING

### Nginx не запускается

```bash
# Проверь синтаксис
sudo nginx -t

# Посмотри ошибки
sudo journalctl -u nginx -n 50

# Проверь порты
sudo lsof -i :80
sudo lsof -i :443
```

### SSL ошибки

```bash
# Проверь пути сертификатов
ls -la /etc/letsencrypt/live/resume.pro/

# Обнови если нужно
sudo certbot renew --dry-run

# Если не работает
sudo certbot certonly --standalone --force-renewal -d resume.pro
```

### Медленный ответ

```bash
# Проверь upstream FastAPI
curl http://127.0.0.1:8000/health

# Посмотри nginx buffers в конфиге
# proxy_buffer_size 4k;
# proxy_buffers 8 4k;
```

---

## ✅ ФИНАЛЬНЫЙ ЧЕКЛИСТ

- [ ] Nginx установлен
- [ ] Конфиг скопирован и проверен (`nginx -t`)
- [ ] Let's Encrypt сертификат установлен
- [ ] Nginx запущен (`systemctl start nginx`)
- [ ] Домен указывает на IP VM
- [ ] HTTPS работает (`curl https://resume.pro`)
- [ ] SSL рейтинг A+ (https://www.ssllabs.com)
- [ ] Rate limiting настроено
- [ ] Логи проверены
