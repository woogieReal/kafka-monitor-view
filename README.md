# kafka-monitor-view

서버의 CPU / Memory 부하를 Kafka를 통해 실시간으로 수집·경고하는 로컬 학습용 프로젝트.

## 개요

- **목적**: 서버의 부하 상태(CPU, Memory)를 실시간으로 측정하고, Kafka를 통해 비동기적으로 처리하여 임계치 초과 시 즉각적인 피드백을 제공
- **핵심 가치**: 데이터 생성(Producer)과 소비(Consumer)의 완전한 분리 및 실시간 스트림 데이터 처리 경험

## 주요 기능

- **Metric Producer**: OS 레벨의 지표(CPU Load Average, Free Memory)를 1초 주기로 수집해 JSON 포맷으로 `system-metrics` 토픽에 발행
- **Alert Consumer**: 토픽을 상시 구독하다가 CPU 사용량이 임계치(1.0)를 초과하면 터미널에 시각적인 경고(🚨) 출력
- **Kafka UI**: 브라우저에서 토픽 상태, 메시지 이력, 컨슈머 그룹 확인 (`http://localhost:8080`)

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
| Zookeeper | 2181 | Kafka 클러스터 메타데이터 관리 및 노드 상태 조율 |
| Kafka1 | 9092 | 메시지 브로커 (BROKER_ID: 1) |
| Kafka2 | 9093 | 메시지 브로커 (BROKER_ID: 2) |
| Kafka3 | 9094 | 메시지 브로커 (BROKER_ID: 3) |
| kafka-init | — | 브로커 준비 완료 후 토픽 생성 전담 컨테이너 (완료 후 종료) |
| Kafka UI | 8080 | 웹 대시보드 |
| Producer | — | OS 지표 수집 및 발행 |
| Consumer | — | 임계치 초과 경고 출력 |

> 브로커 3개 클러스터 구성. `system-metrics` 토픽은 파티션 3개, 레플리카 3개로 설정되어 브로커 1개 장애 시에도 서비스가 유지된다.

## 인프라 설정

### 주요 환경 변수

- **Kafka (각 브로커 공통)**
  - `KAFKA_ADVERTISED_HOST_NAME`: `kafka1` / `kafka2` / `kafka3` (Docker 네트워크 내부 통신 기준; `127.0.0.1`로 설정 시 컨테이너 내부에서 메타데이터 fetch 실패)
  - `KAFKA_AUTO_CREATE_TOPICS_ENABLE`: `false` (kafka-init보다 producer가 먼저 토픽을 auto-create하는 경쟁 조건 차단)
- **kafka-init**
  - `kafka-init/init-topics.sh` 스크립트로 `system-metrics` 토픽 생성 (파티션 3개, 레플리카 3개)
  - `KAFKA_CREATE_TOPICS` 환경변수 대신 init 컨테이너를 사용하는 이유: 브로커 기동 직후 시점에는 다른 브로커가 아직 클러스터에 합류하지 않아 replication-factor=3 설정이 적용되지 않는 타이밍 문제가 있었음
  - producer/consumer는 `depends_on: condition: service_completed_successfully`로 kafka-init 완료 이후에만 기동
- **Kafka UI**
  - `KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS`: `kafka1:9092,kafka2:9092,kafka3:9092`
- **Producer / Consumer**
  - 브로커 연결 주소: `kafka1:9092,kafka2:9092,kafka3:9092` (Docker 네트워크 내부 통신)
  - Kafka보다 먼저 기동될 수 있으므로 `NoBrokersAvailable` 예외 처리 및 재시도 로직 적용

### 실행 환경

- **Docker & Docker Compose**: 컨테이너 기반 인프라 격리 및 실행
- **Resource**: 대량의 데이터를 다루지 않는 로컬 테스트 용도이므로 기본 할당 자원으로 충분

## 실행 방법

```bash
docker compose up -d --build
```

## 재시작

```bash
docker compose down --remove-orphans && docker compose up -d
```

## 디렉토리 구조

```
producer/           # Metric Producer (Python)
consumer/           # Alert Consumer (Python)
kafka-init/         # 토픽 초기화 스크립트 (init-topics.sh)
docker-compose.yml
```
