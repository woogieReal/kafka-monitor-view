## Infrastructure Requirements

### 1. 서비스 구성 (Containers)
*   **Zookeeper**: Kafka 클러스터의 메타데이터 관리 및 노드 상태 조율.
*   **Kafka Broker**: 데이터 스트림을 수집, 저장 및 배포하는 핵심 엔진.
*   **Kafka UI**: 토픽 상태, 메시지 내용, 컨슈머 그룹을 시각적으로 확인하기 위한 웹 대시보드.
*   **Metric Producer**: OS 지표를 수집하여 `system-metrics` 토픽으로 발행하는 컨테이너.
*   **Alert Consumer**: `system-metrics` 토픽을 구독하여 임계치 초과 시 경고를 출력하는 컨테이너.

### 2. 네트워크 및 포트 설정
| Service | Internal Port | External (Host) Port | Description |
| :--- | :--- | :--- | :--- |
| **Zookeeper** | 2181 | `2181` | 클라이언트 연결용 |
| **Kafka** | 9092 | `9092` | Producer/Consumer 통신용 |
| **Kafka UI** | 8080 | `8080` | 웹 브라우저 접속용 |

### 3. 주요 환경 변수 및 설정
*   **Kafka**
    *   `KAFKA_ADVERTISED_HOST_NAME`: `127.0.0.1` (로컬 개발 환경 기준)
    *   `KAFKA_CREATE_TOPICS`: `system-metrics:1:1` (자동 토픽 생성 설정)
*   **Kafka UI**
    *   `KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS`: `kafka:9092` (브로커 연결 주소)
*   **Producer / Consumer**
    *   브로커 연결 주소: `kafka:9092` (Docker 네트워크 내부 통신이므로 `127.0.0.1` 사용 불가)
    *   `KAFKA_ADVERTISED_HOST_NAME`은 반드시 `kafka`로 설정해야 함 (`127.0.0.1`로 설정 시 컨테이너 내부에서 메타데이터 fetch 실패)
    *   Producer/Consumer는 Kafka보다 먼저 뜰 수 있으므로 `NoBrokersAvailable` 예외 처리 및 재시도 로직 필요

### 4. 실행 환경
*   **Docker & Docker Compose**: 컨테이너 기반 인프라 격리 및 실행.이 
*   **Resource**: 대량의 데이터를 다루지 않는 로컬 테스트 용도이므로 기본 할당 자원으로 충분함.