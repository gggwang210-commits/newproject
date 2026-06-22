# 허리통증 프로젝트 위치 재정의

## 결론

허리통증 프로젝트는 LIGHT ONE의 대표 주제가 아닙니다. 이 자료는 과거 교육용 데이터 분석 실험이자, BodyScan AI와 CADSS를 설계할 때 참고한 보조 자료로만 둡니다.

## 왜 낮춰야 하는가

현재 README와 관련 문서가 허리통증/NHANES 중심으로 작성되어 있으면, 심사자는 이 저장소를 “허리통증 예측 AI 프로젝트”로 이해할 가능성이 높습니다. 그러면 LIGHT ONE BODY CARE SYSTEM이라는 창업 아이템의 고객 문제, MVP, 수익모델, 검증 계획이 뒤로 밀립니다.

## 안전한 설명 방식

사용 가능:

- 과거 공개 데이터 기반 교육용 분석 실험
- 자가보고 통증 라벨을 다룰 때 과해석을 피하는 표현 원칙을 정리한 참고자료
- BodyScan AI의 통증 호소 정보 처리에서 의료적 단정을 피하기 위한 선행 학습 자료
- CADSS의 위험 표현 차단 기준을 만들 때 참고한 실험물

피해야 할 표현:

- LIGHT ONE의 핵심 AI 모델
- 허리통증 진단 모델
- 통증 원인 판정 모델
- 치료 또는 운동 처방 엔진
- 정확도 검증 완료 모델

## GitHub 내 권장 위치

```text
docs/archive/backpain_target_definition.md
docs/archive/backpain_presentation_talking_points.md
reports/archive/backpain_final_project_summary.md
references/backpain_experiment/
```

지금 당장 파일을 삭제할 필요는 없습니다. 먼저 README와 제출 문서에서 대표 주제를 LIGHT ONE으로 바꾸고, 허리통증 자료는 “참고/보조/과거 실험”이라고 제목에 명시하는 것이 안전합니다.

## 심사자에게 설명할 한 문장

“허리통증 분석은 메인 창업 아이템이 아니라, 비의료 웰니스 AI가 건강 관련 표현을 다룰 때 어떤 식으로 과해석을 피해야 하는지 검증한 과거 교육용 실험입니다.”
