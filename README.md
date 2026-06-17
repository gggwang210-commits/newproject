<<<<<<< HEAD
# 생활습관 데이터 기반 만성 허리 통증 관련 신호 분석

미래융합교육원 AI 바이오헬스케어 과정 팀 프로젝트용 저장소입니다.

## 프로젝트 목적

NHANES 2009-2010 공개 데이터를 활용하여 생활습관, 체형, 인구사회학적 변수와 자가보고 허리 통증 라벨 사이의 관련 신호를 분석합니다.

본 프로젝트는 교육용 머신러닝 과제이며 의료 진단, 치료 권고, 개인 건강 판단 도구가 아닙니다.

## 핵심 분석 질문

- 신체활동, 좌식시간, 수면시간, 흡연, BMI, 허리둘레 등의 변수가 자가보고 허리 통증 라벨 분류에 어느 정도 기여하는가?
- 단순 기준선 모델 대비 Logistic Regression, Random Forest 모델이 분류 성능을 개선하는가?
- 모델이 중요하게 활용한 변수는 무엇이며, 발표에서 과해석 없이 설명할 수 있는가?

## 데이터 출처

- CDC NHANES 2009-2010 Arthritis Questionnaire: `ARQ_F.XPT`
- CDC NHANES 2009-2010 Physical Activity: `PAQ_F.XPT`
- CDC NHANES 2009-2010 Body Measures: `BMX_F.XPT`
- CDC NHANES 2009-2010 Sleep Disorders: `SLQ_F.XPT`
- CDC NHANES 2009-2010 Smoking - Cigarette Use: `SMQ_F.XPT`
- CDC NHANES 2009-2010 Demographics: `DEMO_F.XPT`

원본 XPT 파일은 저장소에 직접 커밋하지 않는 것을 권장합니다. 각 파일은 `data/raw/`에 로컬로 배치한 뒤 실행합니다.

## 권장 디렉터리 구조

```text
.
├── data/
│   ├── raw/              # 원본 XPT 파일. Git 추적 제외 권장
│   └── processed/        # 전처리된 CSV
├── docs/                 # 타겟 정의, 발표 문구, 검증 문서
├── outputs/              # 모델 성능표, 그래프, 분석 결과
├── reports/              # 요약 보고서, 검증 보고서
├── src/
│   ├── data/             # 전처리 코드
│   └── models/           # 모델 학습 코드
├── requirements.txt
└── README.md
```

## 빠른 실행 순서

### 1. 환경 준비

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell에서는 다음을 사용합니다.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. 원본 데이터 배치

아래 파일을 `data/raw/`에 저장합니다.

```text
ARQ_F.XPT
PAQ_F.XPT
BMX_F.XPT
SLQ_F.XPT
SMQ_F.XPT
DEMO_F.XPT
```

### 3. 전처리 실행

```bash
python src/data/preprocess_nhanes.py --raw-dir data/raw --processed-dir data/processed --outputs-dir outputs --reports-dir reports
```

### 4. 모델 학습 실행

```bash
python src/models/train_models.py --input data/processed/nhanes_backpain_processed.csv --outputs-dir outputs --reports-dir reports
```

## 5일 실행 계획

| 일차 | 핵심 작업 | 완료 기준 | 주요 산출물 |
|---|---|---|---|
| Day 1 | 저장소 구조 정리 및 타겟 정의 고정 | CDC 코드북 기준 타겟 정의 문서화 | `README.md`, `docs/target_definition.md`, `reports/source_verification_report.md` |
| Day 2 | 전처리 코드 개선 및 재현 로그 생성 | 병합 데이터, 결측률, 타겟 분포 산출 | `src/data/preprocess_nhanes.py`, `data/processed/nhanes_backpain_processed.csv`, `reports/preprocessing_summary.csv` |
| Day 3 | 기준 모델 재실행 | Logistic Regression, Random Forest 성능표 생성 | `src/models/train_models.py`, `outputs/model_performance.csv`, ROC/PR/혼동행렬 이미지 |
| Day 4 | 임계값, class weight, ablation 분석 | recall/precision 균형점 및 체형 변수 영향 비교 | `outputs/threshold_comparison.csv`, `outputs/class_weight_comparison.csv`, `outputs/body_measure_ablation.csv` |
| Day 5 | 발표/문서 최종 보정 | 과해석 표현 제거, 재현 수치만 확정값 표기 | `reports/final_project_summary.md`, `docs/presentation_talking_points.md` |

## 표현 원칙

사용 가능 표현:

- 자가보고 허리 통증 라벨
- 허리 통증 관련 신호
- 분류에 기여한 변수
- 모델이 참고한 생활습관/체형 변수
- 단면 설문 데이터 기반 분석

피해야 할 표현:

- 허리 통증 원인
- 진단 모델
- 치료 가이드라인
- 생활습관이 통증을 유발한다
- 개인별 의학적 판단 가능

## 현재 검증 필요 항목

- 실제 XPT 파일 기반 최종 표본 수
- 양성/음성 비율
- 변수별 결측률
- 모델 성능 재현값
- `ARQ024D` 보조 타겟 사용 가능성
- 국민건강영양조사 기반 한국화 가능성
=======
# newproject
>>>>>>> 28b7a0fda7cf22b319e21f08e5483218809f2794
