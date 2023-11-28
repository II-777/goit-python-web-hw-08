---
title: docker-command
date: 2023-11-28 05:33
author: II-777
tags: #docker #rabbitmq
---

## Docker Command to Deploy RabbitMQ
```bash
docker run -it --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```
