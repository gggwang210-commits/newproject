# LIGHT ONE 중심 GitHub 정리안

## 1. 현재 판단

현재 저장소는 심사자 관점에서 LIGHT ONE 창업 저장소로 읽히지 않습니다. README, 발표 문장, 요약 보고서, 검증 보고서가 모두 NHANES 기반 허리통증 분석을 대표 프로젝트처럼 설명하고 있습니다.

모두의창업 2차 관점에서는 기술 실험 자체보다 다음 네 가지가 먼저 보여야 합니다.

1. 어떤 고객의 문제를 해결하는가
2. 어떤 MVP를 이미 만들었는가
3. 누가 첫 고객이 될 수 있는가
4. 어떤 방식으로 검증하고 보완했는가

## 2. 정리 원칙

| 항목 | 기존 위치 | 변경 방향 |
|---|---|---|
| LIGHT ONE | 외부 Netlify 링크 중심 | GitHub 첫 화면의 대표 주제 |
| BodyScan AI | 별도 기술 데모 | LIGHT ONE 내부 분석 엔진 |
| CADSS | 별도 안전 페이지 | AI 출력 검토·위험 라우팅 보완 장치 |
| 허리통증 프로젝트 | README 대표 주제 | 과거 실험 또는 참고 프로젝트 |
| NHANES 데이터 | 핵심 데이터 근거 | 교육용 분석 참고 근거 |

## 3. 권장 폴더 구조

```text
.
├── README.md                         # LIGHT ONE 메인 README로 교체
├── README_LIGHTONE_DRAFT.md           # 교체 전 검토용 초안
├── docs/
│   ├── lightone_github_restructure_plan.md
│   ├── modu_startup_round2_checklist.md
│   ├── product_overview.md
│   ├── mvp_validation_plan.md
│   ├── customer_interview_script.md
│   ├── risk_expression_policy.md
│   └── archive/
│       ├── backpain_target_definition.md
│       └── backpain_presentation_talking_points.md
├── references/
│   └── backpain_experiment/
├── src/
│   └── backpain_project/              # 지금은 유지하되 reference로 설명
└── reports/
    └── backpain_final_project_summary.md
```

비전공자 기준으로 말하면, 코드를 당장 지우는 것이 아니라 “간판”을 바꾸고 “과거 자료”를 뒤쪽 서랍으로 옮기는 작업입니다.

## 4. 우선 수정 대상 파일

| 우선순위 | 파일 | 현재 문제 | 조치 |
|---|---|---|---|
| 1 | `README.md` | 허리통증 AI 프로젝트가 대표 제목 | LIGHT ONE BODY CARE SYSTEM 중심으로 교체 |
| 2 | `docs/presentation_talking_points.md` | 발표 핵심 문장이 허리통증/NHANES 중심 | 모두의창업 2차 발표 문장으로 재작성 |
| 3 | `reports/final_project_summary.md` | 최종 요약이 교육용 머신러닝 프로젝트 | 창업 아이템 요약으로 재작성 |
| 4 | `docs/target_definition.md` | 타겟 변수 정의 문서가 대표 문서처럼 보임 | `docs/archive/`로 이동 또는 제목에 과거 실험 명시 |
| 5 | `reports/source_verification_report.md` | CDC 데이터 근거가 메인 근거처럼 보임 | BodyScan/CADSS/시장검증 근거 문서와 분리 |
| 6 | `VISUAL_STUDIO_START.md` | 실행 안내가 허리통증 코드 기준일 가능성 | LIGHT ONE 문서 작업 안내 또는 참고 코드 실행 안내로 변경 |

## 5. README 교체 후 첫 화면 메시지

첫 화면은 다음 순서로 보여야 합니다.

1. LIGHT ONE이 무엇인지 한 문장
2. 누구를 위한 서비스인지
3. 어떤 문제를 해결하는지
4. 현재 공개된 데모 링크 4개
5. 사용 흐름
6. MVP와 검증 계획
7. BodyScan AI와 CADSS의 역할
8. 과거 허리통증 프로젝트는 참고자료라고 명시

## 6. 허리통증 문구 처리 기준

삭제하지 말아야 할 것:

- 데이터 분석 실험 이력
- 의료적 과해석을 피하려고 정리한 표현 원칙
- 공개 데이터 기반 모델링 경험

낮춰야 할 것:

- 프로젝트 대표 제목
- 메인 README 첫 문단
- 모두의창업 제출 자료의 중심 근거
- “허리통증 위험도 예측”처럼 의료적으로 오해될 수 있는 문구

## 7. 심사자 관점의 핵심 메시지

“이 창업자는 단순 아이디어가 아니라, 실제 데모 페이지와 GitHub 문서, 기술 보완 장치, 검증 계획을 묶어 MVP로 정리하고 있다.”

이 메시지가 보이면 2차에서 유리합니다. 반대로 GitHub 첫 화면이 허리통증 교육용 분석으로 보이면, LIGHT ONE의 사업성과 실행 증거가 흐려집니다.
