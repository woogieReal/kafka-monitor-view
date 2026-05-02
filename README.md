# kafka-monitor-view

서버의 CPU / Memory 부하를 Kafka를 통해 실시간으로 수집·경고하는 로컬 학습용 프로젝트.

## 개요

- **Metric Producer**: OS 지표(CPU, Memory)를 1초 주기로 수집해 `system-metrics` 토픽에 발행
- **Alert Consumer**: 토픽을 상시 구독하다가 CPU 사용량이 임계치(1.0)를 초과하면 터미널에 경고 출력
- **Kafka UI**: 브라우저에서 토픽 상태와 메시지 이력 확인 (`http://localhost:8080`)

## 메시지 스키마

```json
{
  "timestamp": "2026-05-01T16:46:00Z",
  "node_id": "local-mac-mini",
  "metrics": {
    "cpu_usage": 1.25,
    "mem_free_bytes": 1073741824
  }
}
```

## 서비스 구성

| Service | Port | 설명 |
| :--- | :--- | :--- |
| Zookeeper | 2181 | Kafka 메타데이터 관리 |
| Kafka1 | 9092 | 메시지 브로커 (BROKER_ID: 1) |
| Kafka2 | 9093 | 메시지 브로커 (BROKER_ID: 2) |
| Kafka3 | 9094 | 메시지 브로커 (BROKER_ID: 3) |
| Kafka UI | 8080 | 웹 대시보드 |
| Producer | — | OS 지표 수집 및 발행 |
| Consumer | — | 임계치 초과 경고 출력 |

> 브로커 3개 클러스터 구성. `system-metrics` 토픽은 레플리카 3개로 설정되어 브로커 1개 장애 시에도 서비스가 유지된다.

## 실행 방법

```bash
docker compose up --build
```

## 디렉토리 구조

```
producer/       # Metric Producer (Python)
consumer/       # Alert Consumer (Python)
docs/           # 기획 및 설계 문서
docker-compose.yml
```
