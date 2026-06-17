# Visual Studio Code 실행 안내

이 ZIP은 VS Code에서 바로 열 수 있도록 구성한 프로젝트 패키지입니다.

## 1. 압축 해제

원하는 위치에 압축을 해제한 뒤 `newproject_visualstudio_ready` 폴더를 VS Code에서 엽니다.

## 2. Python 가상환경 생성

PowerShell 터미널에서 실행합니다.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. 원본 데이터 배치

아래 NHANES XPT 파일을 `data/raw/`에 넣습니다.

```text
ARQ_F.XPT
PAQ_F.XPT
BMX_F.XPT
SLQ_F.XPT
SMQ_F.XPT
DEMO_F.XPT
```

## 4. 전처리 실행

```powershell
python src/data/preprocess_nhanes.py --raw-dir data/raw --processed-dir data/processed --outputs-dir outputs --reports-dir reports
```

## 5. 모델 학습 실행

```powershell
python src/models/train_models.py --input outputs/nhanes_backpain_processed.csv --outputs-dir outputs --reports-dir reports
```

## 6. GitHub 업로드

```powershell
git init
git add .
git commit -m "Initialize NHANES back pain analysis project scaffold"
git branch -M main
git remote add origin https://github.com/gggwang210-commits/newproject.git
git push -u origin main
```

이미 clone 받은 저장소 안에서 사용할 경우에는 압축 해제한 내부 파일만 저장소 루트로 복사한 뒤 아래만 실행합니다.

```powershell
git add .
git commit -m "Initialize NHANES back pain analysis project scaffold"
git push origin main
```
