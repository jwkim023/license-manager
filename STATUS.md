# License Manager — 개발 현황

> 기준일: 2026-05-05

---

## 실행 방법

```bash
# 최초 실행 (이미지 빌드 + DB 마이그레이션 + 서버 기동)
docker-compose up --build -d

# 코드 변경 후 반영
docker-compose up --build -d

# 종료
docker-compose down

# DB 데이터까지 완전 삭제
docker-compose down -v
```

---

## 접속 URL

| 용도 | URL |
|------|-----|
| 라이선스 관리 화면 | http://localhost:8000 |
| Swagger UI (API 테스트) | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

---

## 현재 동작하는 기능

### 화면 (Jinja2 + HTMX + Bootstrap 5)

| 기능 | 동작 |
|------|------|
| 라이선스 목록 조회 | `GET /` — 전체 목록 테이블 |
| 새 라이선스 등록 | "새 라이선스" 버튼 → 모달 폼 → 저장 시 목록 갱신 |
| 라이선스 수정 | "수정" 버튼 → 기존 값 채워진 모달 폼 → 저장 시 목록 갱신 |
| 라이선스 삭제 | "삭제" 버튼 → 확인 다이얼로그 → 삭제 후 목록 갱신 |
| 만료 임박 표시 | 만료일 30일 이내 항목 빨간색 + D-day 표시 |
| 상태 뱃지 | 활성(초록) / 만료(빨강) / 해지(회색) |

> 모든 화면 조작은 페이지 이동 없이 부분 갱신(HTMX)으로 동작합니다.

---

### API (JSON)

#### 라이선스 (`/licenses`)

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/licenses/` | 전체 목록 (status, department 필터 가능) |
| `GET` | `/licenses/{id}` | 단건 조회 |
| `POST` | `/licenses/` | 등록 |
| `PUT` | `/licenses/{id}` | 수정 |
| `DELETE` | `/licenses/{id}` | 삭제 |

#### 히스토리 (`/history`)

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/history/` | 변경 이력 조회 (entity_type, entity_id 필터, limit 최대 200) |

> 라이선스 등록/수정/삭제 시 변경 이력이 자동으로 기록됩니다.

---

### DB 테이블 (PostgreSQL 15)

| 테이블 | 설명 |
|--------|------|
| `licenses` | 라이선스 (제품명, 계정, 담당자, 부서, 수량, 만료일, 상태, 비고) |
| `employees` | 조직/임직원 (Azure AD 구조, 자기참조 상위관리자) |
| `history` | 변경 이력 (entity_type, entity_id, action, before/after JSON) |

---

## 미구현 (남은 Phase)

| Phase | 내용 | 상태 |
|-------|------|------|
| Phase 4 | Azure AD 연동 — 조직도/임직원 동기화 (`services/azure_ad.py`) | 미구현 |
| Phase 5 | Brity 알림 연동 — 만료 알림 메시지 발송 (`services/brity.py`) | 미구현 |
| Phase 6 | 히스토리 조회 화면 — 필터/페이징 UI | 미구현 |
| Phase 7 | Dockerfile 최적화, 운영 배포 | 부분 완료 |

---

## 기술 스택

| 구분 | 사용 기술 |
|------|-----------|
| 백엔드 | FastAPI, SQLAlchemy 2, Alembic, Pydantic v2 |
| 프론트엔드 | Jinja2, HTMX 1.9, Bootstrap 5.3 |
| DB | PostgreSQL 15 |
| 인프라 | Docker, docker-compose |
| 예정 연동 | Azure AD (MSAL), Brity |
