# License Manager 개발 순서 가이드

---

## Phase 1. 기반 환경 구성

1. **가상환경 생성 및 패키지 설치** — `requirements.txt` 기반
2. **PostgreSQL 실행** — `docker-compose up -d db` 로 DB 컨테이너 먼저 띄우기
3. **`.env` 작성** — DB 접속정보 먼저, Azure/Brity는 나중에
4. **Alembic 초기화** — `alembic init alembic`, `env.py`에 SQLAlchemy 연결 설정

---

## Phase 2. DB 모델 설계 및 마이그레이션

1. **`models/license.py`** — 라이선스 테이블 (제품명, 계정, 담당자, 만료일 등)
2. **`models/organization.py`** — 조직/임직원 테이블 (Azure AD 구조 맞게)
3. **`models/history.py`** — 변경 이력 테이블 (변경일시, 변경자, 변경 전/후 값)
4. **Alembic 마이그레이션 실행** — 테이블 생성 확인
5. **Spotfire 연결 테스트** — 이 시점에 PostgreSQL ODBC 접속이 가능한지 확인

---

## Phase 3. 라이선스 CRUD (핵심 기능)

1. **`routers/license.py`** — GET/POST/PUT/DELETE API 구현
2. **`services/history.py`** — 라이선스 변경 시 자동으로 히스토리 기록하는 로직
3. **`templates/`** — 라이선스 목록/등록/수정 화면 (Jinja2 + HTMX)
4. **동작 확인** — Swagger UI(`/docs`)로 API 테스트

---

## Phase 4. Azure AD 연동

1. **Azure 앱 등록** — Azure Portal에서 앱 등록, `client_id` / `client_secret` / `tenant_id` 발급
2. **`services/azure_ad.py`** — MSAL로 토큰 획득, Graph API로 조직도/임직원 조회
3. **`routers/organization.py`** — 조직 동기화 API (Azure에서 가져와서 DB에 upsert)
4. **`templates/`** — 조직 현황 화면 및 수동 동기화 버튼

---

## Phase 5. Brity 알림 연동

1. **Brity API 스펙 확인** — 인증 방식, 메시지 발송 엔드포인트 파악
2. **`services/brity.py`** — API 호출 로직 구현
3. **`routers/notification.py`** — 발송 대상/내용 지정 후 메시지 발송 API
4. **`templates/`** — 발송 화면 (대상자 선택, 메시지 미리보기)

---

## Phase 6. 히스토리 조회 화면

1. **`routers/history.py`** — 필터(기간, 변경자, 대상) 조회 API
2. **`templates/`** — 히스토리 목록 화면 (페이징, 필터 UI)

---

## Phase 7. 마무리

1. **Docker 전체 빌드** — `Dockerfile` 작성 후 `docker-compose up` 전체 기동
2. **`.env` 보안 처리** — `.gitignore`에 `.env` 추가
3. **운영 배포** — 사내 서버 또는 VM에 배포

---

## 권장 개발 우선순위 요약

```
DB 모델 → 라이선스 CRUD → Azure AD → Brity → 히스토리 화면
```

Phase 2~3까지만 완성해도 엑셀 대체 시스템으로 바로 사용 가능하고,
이후 외부 연동(Azure, Brity)을 붙이는 방식으로 단계적으로 확장하는 걸 추천합니다.
