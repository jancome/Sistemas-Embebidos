# Semana 09 – HTTP y MQTT

**Fecha:** 30 de septiembre de 2026 · **Fase 2**

## Recurso principal

- [Marco teórico: protocolos HTTP y MQTT](marco-teorico.md)

## Pregunta guía

¿Cómo intercambiar datos sin confundir el protocolo, el formato del mensaje y la lógica de aplicación?

## Resultados

- Diferenciar solicitud/respuesta y publicación/suscripción.
- Construir payloads claros.
- Interpretar códigos de respuesta.
- Manejar tiempo de espera y fallas.

## Contenidos

- HTTP GET y POST.
- Cabeceras, cuerpo y JSON.
- MQTT: broker, tópico, QoS y mensajes.
- Latencia, memoria y reintentos.
- Credenciales fuera del código público.

## Laboratorio

Publicar temperatura, humedad u otra variable usando HTTP o MQTT. Registrar tiempo, respuesta, tamaño del payload y comportamiento cuando el servicio no está disponible.

## Evidencia ABP

- Diagrama de comunicación.
- Payload documentado.
- Captura de envío y recepción.
- Manejo de error y recuperación.
