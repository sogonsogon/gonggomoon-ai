# gonggomoon-ai (MVP)

현재 프로젝트는 아래 최소 기능 플로우를 기준으로 동작합니다.

1. `POST /api/v1/jobs/{ai_function}` 요청 수신
2. Redis queue 에 작업 enqueue
3. Worker 가 dequeue 후 파일 다운로드/LLM 분석
4. 분석 결과를 callback URL 로 POST

## Run

- Redis 필요: `REDIS_URL` (기본값 `redis://localhost:6379/0`)
- API 서버: `uv run python main.py`
- 워커: `uv run python app.worker.main`

## Docker Compose

1. 환경 변수 파일 생성: `cp .env.example .env`
2. 컨테이너 시작: `docker compose up --build`
3. API 확인: `http://localhost:8000/health`

- API: `api` 서비스 (`8000` 포트)
- Worker: `worker` 서비스
- Redis: `redis` 서비스

