# 생활습관 기반 허리통증 위험군 탐색 AI 프로젝트

공개 설문 데이터와 생활습관·체형 변수를 활용해 자가보고 허리통증 위험군을 탐색하는 교육용 AI MVP입니다.

이 프로젝트는 의료 진단 앱이 아닙니다. 결과는 포트폴리오·교육·발표용 참고 정보이며, 진단·치료·처방·임상 의사결정을 대체하지 않습니다.

## 1. 프로젝트 개요

이 저장소는 허리통증 관련 생활습관 신호를 탐색하기 위한 실행 가능한 Python/FastAPI 프로젝트입니다.

주요 기능은 다음과 같습니다.

- 생활습관·체형 입력값 기반 허리통증 위험도 예측 데모
- FastAPI 기반 `/predict` API 제공
- Swagger UI를 통한 API 테스트
- 발표 자료, 요약 문서, 검증 체크리스트 포함
- 의료적 과해석을 줄이기 위한 disclaimer 포함

## 2. 문제 정의

허리통증은 다양한 생활습관, 체형, 수면, 활동량 요인과 함께 관찰될 수 있습니다. 이 프로젝트는 공개 설문 데이터를 활용해 특정 변수가 자가보고 허리통증 라벨과 어떤 관련 신호를 보이는지 탐색합니다.

단, 본 프로젝트는 단면 설문 데이터 기반 탐색 프로젝트입니다. 따라서 인과관계, 진단 정확도, 치료 효과를 주장하지 않습니다.

## 3. 사용 데이터

프로젝트 자료에는 NHANES 2009-2010 관련 원본 XPT 파일과 샘플 CSV가 포함되어 있습니다.

주요 파일 예시는 다음과 같습니다.

```text
data/raw/ARQ_F.XPT
data/raw/BMX_F.XPT
data/raw/DEMO_F.XPT
data/raw/PAQ_F.XPT
data/raw/SLQ_F.XPT
data/raw/SMQ_F.XPT
data/sample/backpain_sample.csv
```

포트폴리오 설명에서는 “공개 설문 데이터 기반 자가보고 허리통증 위험군 탐색”으로 표현하는 것이 안전합니다.

## 4. 주요 입력 변수

API 입력값은 다음 변수를 사용합니다.

```json
{
  "age": 58,
  "gender": "male",
  "bmi": 31,
  "waist_cm": 102,
  "sedentary_hours": 10,
  "sleep_hours": 5,
  "smoking_status": "current"
}
```

입력 변수 설명:

| 변수 | 의미 |
|---|---|
| `age` | 나이 |
| `gender` | 성별 |
| `bmi` | 체질량지수 |
| `waist_cm` | 허리둘레(cm) |
| `sedentary_hours` | 하루 좌식 시간 |
| `sleep_hours` | 수면 시간 |
| `smoking_status` | 흡연 상태 |

## 5. 프로젝트 구조

```text
backpain_project_package/
├── config/
│   └── data_contract.yaml
├── data/
│   ├── raw/
│   └── sample/
├── demo_app/
│   └── index.html
├── docs/
├── presentation/
├── scripts/
│   ├── run_demo_prediction.py
│   ├── verify_package.py
│   └── verify_target_definition.py
├── src/
│   └── backpain_project/
│       ├── api.py
│       ├── predict.py
│       ├── risk_text.py
│       ├── schemas.py
│       └── train_model.py
├── README.md
└── requirements.txt
```

## 6. 실행 방법

### 6.1 가상환경 생성 및 활성화

Windows PowerShell 기준:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

이미 가상환경이 있다면 활성화만 하면 됩니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

### 6.2 패키지 설치

```powershell
python -m pip install -r requirements.txt
```

### 6.3 프로젝트 구조 검증

```powershell
python scripts/verify_package.py
```

정상 결과:

```text
package structure check passed
```

### 6.4 데모 예측 실행

```powershell
python scripts/run_demo_prediction.py
```

정상 실행 시 `probability`, `risk_band`, `related_signals`, `disclaimer`가 출력됩니다.

### 6.5 FastAPI 서버 실행

```powershell
uvicorn src.backpain_project.api:app --reload
```

브라우저에서 다음 주소를 엽니다.

```text
http://127.0.0.1:8000/docs
```

Swagger UI에서 `POST /predict`를 열고 `Try it out` → `Execute` 순서로 API를 테스트할 수 있습니다.

## 7. API 테스트 예시

Swagger의 `POST /predict` 입력창에 아래 JSON을 넣습니다.

```json
{
  "age": 58,
  "gender": "male",
  "bmi": 31,
  "waist_cm": 102,
  "sedentary_hours": 10,
  "sleep_hours": 5,
  "smoking_status": "current"
}
```

예상 응답 구조:

```json
{
  "probability": 0.7,
  "risk_band": "높음",
  "related_signals": [
    "연령대가 모델 입력에서 높은 쪽에 속합니다.",
    "BMI가 샘플 기준 높은 구간에 있습니다."
  ],
  "disclaimer": "본 결과는 교육용 데이터 분석과 포트폴리오 데모를 위한 참고 정보입니다..."
}
```

입력값에 따라 `probability`, `risk_band`, `related_signals`는 달라질 수 있습니다.

## 8. 포함 산출물

| 구분 | 경로 |
|---|---|
| 발표자료 | `presentation/backpain_final_presentation.pptx` |
| 최종 요약 문서 | `docs/final_project_brief.docx` |
| 브라우저용 요약 문서 | `docs/final_project_brief.html` |
| 발표 대본 | `docs/presentation_script.md` |
| 검증 체크리스트 | `docs/validation_checklist.md` |
| 타깃 정의 문서 | `docs/target_definition_v3.md` |
| 한국형 확장 계획 | `docs/korean_extension_plan.md` |
| 브라우저 데모 | `demo_app/index.html` |
| 실행 코드 | `src/backpain_project/` |

## 9. 표현 원칙

사용 가능한 표현:

- 위험군 탐색
- 자가보고 허리통증 관련 신호
- 생활습관·체형 변수 기반 예측 데모
- 교육용 MVP
- 포트폴리오용 분석 프로젝트

피해야 할 표현:

- 진단
- 치료 권고
- 원인 규명
- 의학적으로 확정
- 한국인 검증 완료
- 개인별 의료 판단 가능

## 10. 한계 및 개선 방향

현재 한계:

- 공개 설문 데이터 기반이므로 인과관계를 판단할 수 없습니다.
- 자가보고 라벨을 사용하므로 실제 임상 진단과 다를 수 있습니다.
- 현재 모델은 교육용 MVP이며 의료기기 또는 임상 의사결정 지원 도구가 아닙니다.
- 샘플 기반 데모는 실제 서비스 수준의 검증을 거치지 않았습니다.

개선 방향:

- 국민건강영양조사 등 한국형 데이터 확장 검토
- 통증 부위, 지속 기간, 운동 습관, 직업 요인 등 입력 변수 확장
- 모델 성능 평가 지표 정리
- 프론트엔드 입력 화면 고도화
- 체형분석 서비스와 연동 가능성 검토
- 개인정보 보호 및 의료적 표현 검수 체계 추가

## 11. Git 작업 흐름

수정 후 GitHub에 반영할 때는 아래 순서를 사용합니다.

```powershell
git status
git add .
git commit -m "Update project documentation"
git push
```

## 12. 의료 면책 문구

본 결과는 교육용 데이터 분석과 포트폴리오 데모를 위한 참고 정보입니다. 의료 진단, 치료 권고, 임상 의사결정 지원을 대체하지 않습니다. 통증이나 건강 우려가 있으면 자격을 갖춘 의료 전문가와 상담하세요.
