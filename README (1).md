# 엔화 알림 설정 가이드

구성
- `index.html`: 휴대폰 홈 화면에 추가해서 쓰는 엔화 확인 웹앱 (방식 1)
- `check.py`, `.github/workflows/yen-alert.yml`: 10분마다 확인 후 텔레그램 알림 (방식 2)

## 1. GitHub 저장소 만들기
1. github.com에서 새 저장소(예: `yen-alert`)를 만듭니다. Public 또는 Private 모두 가능합니다.
2. 이 폴더의 파일을 전부 업로드합니다 (`.github` 폴더 포함).
3. 저장소 Settings → Pages → Source를 `Deploy from a branch`, branch를 `main` / `/ (root)`로 설정합니다. 몇 분 뒤 `https://<아이디>.github.io/yen-alert/` 주소가 생깁니다. (Private 저장소는 Pages가 유료 플랜에서만 가능하므로 Public을 권장합니다.)
4. Settings → Actions → General에서 Workflow permissions를 `Read and write permissions`로 바꿉니다.

## 2. 텔레그램 봇 만들기 (방식 2)
1. 텔레그램에서 `@BotFather`와 대화를 시작하고 `/newbot`을 입력합니다. 봇 이름을 정하면 `TOKEN`을 줍니다.
2. 만든 봇에게 아무 메시지나 한 번 보냅니다.
3. 브라우저에서 `https://api.telegram.org/bot<TOKEN>/getUpdates`를 열고 `"chat":{"id": 숫자}` 값을 확인합니다. 이 숫자가 `CHAT_ID`입니다.
4. GitHub 저장소 Settings → Secrets and variables → Actions에 두 개를 추가합니다.
   - `TELEGRAM_TOKEN`: 1단계 토큰
   - `TELEGRAM_CHAT_ID`: 3단계 숫자

## 3. 기준 금액 바꾸기
- 웹앱(`index.html`): 화면에서 직접 입력하고 저장합니다.
- 텔레그램 알림: `.github/workflows/yen-alert.yml`의 `THRESHOLD`(기준, 기본 900원)와 `CHANGE_ALERT`(직전 대비 변동 알림 기준, 기본 3원)를 수정합니다.

## 4. 동작 확인
- 저장소 Actions 탭에서 `yen-alert`를 선택하고 `Run workflow`를 누르면 바로 한 번 실행됩니다.
- 이후에는 10분마다 자동 실행됩니다. GitHub 예약 실행은 부하에 따라 몇 분씩 늦을 수 있습니다.

## 5. 휴대폰에 앱처럼 설치하기 (방식 1)
- iPhone: Safari로 Pages 주소를 열고 공유 버튼 → `홈 화면에 추가`. 알림은 iOS 16.4 이상에서 홈 화면 앱으로 실행했을 때 동작합니다.
- Android: Chrome으로 열고 메뉴 → `홈 화면에 추가` 또는 `앱 설치`.
- 웹앱은 화면이 켜져 있거나 앱이 열려 있을 때 10분마다 확인합니다. 꺼져 있어도 알림을 받으려면 2번(텔레그램)을 함께 쓰세요.

## 참고
- 환율은 open.er-api.com 무료 API를 씁니다. 실제 송금 환율과는 차이가 있으니 참고용으로만 보세요.
- 알림이 너무 자주 오지 않도록 기준 이하일 때는 한 번만, 다시 올라갔다 내려올 때 재알림합니다.
