---
name: esp32-pro-master-skill
description: ESP32 Pro Master Skill - Engenharia de Firmware Avançada
---

# ESP32 Pro Master Skill

## 1. Overview
Esta skill transforma Cindy em uma Engenheira de Firmware Sênior focada no ecossistema Espressif. Ela cobre decisões de arquitetura, otimização de recursos, segurança de nível industrial e conectividade moderna.

## 2. Arquitetura e Seleção de SoC 

### Famílias Principais
*   **ESP32 (Classic):** Dual-core Xtensa LX6. Robusto, legado, mas ainda potente. Ótimo custo-benefício para tarefas gerais.
*   **ESP32-S Series (S2, S3):** 
    *   **S3:** Dual-core Xtensa LX7 + Instruções Vetoriais (IA/DSP) + 45 GPIOs. O "topo de linha" para HMI e Áudio.
*   **ESP32-C Series (C2, C3, C6):** RISC-V. 
    *   **C3:** Substituto do ESP8266, pin-compatible em muitos casos.
    *   **C6:** WiFi 6 + Matter + Thread + Zigbee (802.15.4). O futuro da Smart Home.
*   **ESP32-H Series (H2):** RISC-V, sem WiFi. Focado em 802.15.4 (Matter/Thread/Zigbee) e Bluetooth 5.3.

### Gestão de Memória
*   **SRAM Interna (520KB):** Espaço precioso. Evite `malloc/free` repetitivos para prevenir fragmentação.
*   **PSRAM (SPI RAM):** Use para buffers de áudio, datasets de IA ou display. Habilite em `sdkconfig`: `CONFIG_SPIRAM_BOOT_INIT`.

## 3. Frameworks e Fluxo Profissional

### ESP-IDF (Official SDK) - **RECOMENDADO**
O padrão para projetos escaláveis e comerciais.
- **Build System:** Baseado em CMake. 
- **Componentes:** Use `idf.py create-component` para modularizar o código.
- **Configuração:** `idf.py menuconfig` (Kconfig). Defina partições em `partitions.csv`.
- **Event Loop:** Use `esp_event_loop_with_args` para tratar WiFi, IP e eventos customizados de forma assíncrona.

### Arduino Core (para Prototipagem Rápida)
Embora simplificado, pode ser otimizado:
- **FreeRTOS Nativo:** Sempre use `xTaskCreatePinnedToCore` para evitar que o WiFi (Core 0) sofra interferência da sua lógica (Core 1).
- **StackSize:** Se o chip resetar com `Stack Overflow`, aumente de 2048 para 4096+ em tarefas que usam `printf` ou JSON.

## 4. Eficiência Energética (Low Power)

### Modos de Sleep
*   **Light Sleep:** Mantém estado da RAM. Wakeup rápido (~1ms).
*   **Deep Sleep:** Desliga núcleos principais. Corrente < 10uA.
    *   **RTC RAM:** Variáveis marcadas com `RTC_DATA_ATTR` sobrevivem ao Deep Sleep.
    *   **Wakeup Sources:** Timer, Ext0 (1 pino), Ext1 (vários pinos), ULP Co-processor.
*   **ULP (Ultra Low Power):** Use o co-processador (FSM ou RISC-V dependendo do SoC) para monitorar sensores (I2C/ADC) enquanto o SoC principal dorme.

## 5. Conectividade de Missão Crítica

### WiFi
- **Modo Estático:** Use IP estático para reduzir o tempo de reconexão em 3-5 segundos.
- **WiFi Events:** Monitore `WIFI_EVENT_STA_START` e `IP_EVENT_STA_GOT_IP` via handlers, não via polling.
- **ESP-NOW:** Protocolo proprietário sem conexão para latência mínima e baixo consumo entre placas.

### BLE e Matter
- **BLE GATT:** Defina Services e Characteristics de forma eficiente.
- **Matter:** Implementação sobre WiFi ou Thread. Exige ESP32-S3 ou C6.

## 6. Segurança e Operação Industrial

### Blindagem (Hardening)
- **Secure Boot V2:** Garante que apenas seu firmware assinado rode na placa após o primeiro flash.
- **Flash Encryption:** Encripta o código na Flash QSPI externa, impedindo dumping de firmware por atacantes.
- **NVS Encryption:** Proteja chaves de API e credenciais WiFi gravadas na Partição NVS.

### Sustentabilidade (OTA)
- **A/B Partitioning:** Sempre tenha duas partições OTA para fallback.
- **Rollback:** Ative a verificação de sanidade do firmware (`esp_ota_mark_app_valid_cancel_rollback`) para evitar que a placa fique "tijolada" (bricked) após um update falho.

## 7. Hardware & GPIO Gotchas (Sentivis Checklist)
1. **Strapping Pins:** GPIO0, 2, 5, 12, 15 alteram o boot. Cuidado ao colocar pull-ups/downs externos neles.
2. **Flash Pins:** Nunca use GPIO 6 a 11 (ESP32-D0WD). O sistema trava instantaneamente.
3. **ADC2:** Não funciona com WiFi ativo. Use apenas ADC1 (GPIOs 32-39) se precisar de sensores analógicos e internet simultâneos.
4. **Power Spikes:** WiFi consome até 300-400mA em picos. Sua fonte 3.3V deve ter capacitores de desacoplamento robustos (mínimo 10uF + 100nF).

## 8. Workflow de Resolução
Para qualquer bug de ESP32:
1. Verifique o **Backtrace** no monitor serial (`addr2line`).
2. Identifique se houve **Task Watchdog Timeout** (loop infinito sem yield).
3. Verifique a tensão de entrada durante o pico de boot/WiFi (**Brown-out Detector**).
