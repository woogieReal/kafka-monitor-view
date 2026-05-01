## Application Planning

### 1. 개요 (Overview)
*   **목적**: 서버의 부하 상태(CPU, Memory)를 실시간으로 측정하고, 카프카를 통해 비동기적으로 처리하여 임계치 초과 시 즉각적인 피드백을 제공함.
*   **핵심 가치**: 데이터 생성(Producer)과 소비(Consumer)의 완전한 분리 및 실시간 스트림 데이터 처리 경험.

### 2. 주요 기능 (Core Functions)
*   **Metric Producer**:
    *   OS 레벨의 지표(CPU Load Average, Free Memory) 수집.
    *   1초 주기로 JSON 포맷의 메시지를 `system-metrics` 토픽으로 발행.
*   **Alert Consumer**:
    *   토픽을 상시 구독하여 유입되는 지표를 파싱.
    *   CPU 사용량이 1.0(평균 부하)을 초과할 경우 터미널에 시각적인 경고(🚨) 출력.
*   **Persistence & Visibility**:
    *   카프카 브로커에 저장된 최근 데이터는 Kafka UI를 통해 이력 확인 가능.

### 3. 데이터 스키마 (Message Format)
```json
{
  "timestamp": "2026-05-01T16:46:00Z",
  "node_id": "local-mac-mini",
  "metrics": {
    "cpu_usage": 1.25,
    "mem_free_bytes": 1073741824
  }
}