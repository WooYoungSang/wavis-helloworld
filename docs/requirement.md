# Don’t Press Button — SSOT v1.0 (MVP)

## A. 메타데이터 (GraphRAG/문맥화 헤더)

* **DocID**: SSOT-DPB-MVP-v1.0
* **Domain**: Web UI / Micro Interaction / Modal Flow
* **Scope**: 단일 페이지(SPA 수준의 단순 DOM 조작 가능)
* **Primary Language**: UI 혼합(영어 버튼문구, 한국어 경고문 랜덤 카피), 결제 확인 팝업은 **영어**
* **Target**: Desktop·Mobile Web (반응형 최소 대응)
* **Config Source**: `./config/app.config.json` (문구/카운트/팝업 텍스트 관리)
* **Priority**: P0(MVP 전부)
* **Out of Scope**: 실제 결제 처리/PG 연동, 사용자 인증, 서버 사이드 상태 저장

---

## B. 개요(Overview)

* 중앙 상단에 \*\*조악한 느낌의 텍스트 “Don't Press Button”\*\*가 보이고, 아래에 **빨간색 큰 버튼**이 있습니다.
* 버튼을 클릭할 때마다 버튼 **윗 공간**에 “누르지 말라 했는데 왜 눌렀냐” 뉘앙스의 **영어 랜덤 문구**가 1개 노출됩니다.
* **10번째 클릭 시** 영어로 된 결제 확인 팝업 `"Would you like to proceed with payment?"`가 뜹니다.

  * **Yes** → `"Payment completed"` 팝업(알림) 표시
  * **No** → 아무 일도 일어나지 않음(상태 변화 없음)

---

## C. 기능 요구사항(Functional Requirements, FR)

**FR-1. 헤더 문구 표기**

* 화면 상단에 조악한 스타일(의도적인 폰트/스타일 적용)로 **“Don't Press Button”** 텍스트를 표시한다.

**FR-2. 빨간 버튼 렌더링**

* 텍스트 아래에 **빨간색(brand-red)** 버튼을 배치한다.
* 버튼 라벨: `"Don't Press Button"` (영어)

**FR-3. 클릭 카운팅 & 랜덤 경고 출력**

* 버튼 클릭 시 **클릭 카운트**를 +1 한다.
* 매 클릭마다 버튼 **윗 공간**에 경고 문구를 **랜덤 1개** 출력(중복 허용).
* 경고 문구는 **한국어**(뉘앙스: “누르지 말라니까 왜 눌러?”류).
  예시(가이드 20개):

  1. “분명 누르지 말랬죠?”
  2. “왜 누르셨나요…?”
  3. “다음엔 참아볼까요?”
  4. “진짜 누르지 말랬는데요.”
  5. “혹시 경고를 못 보신 건가요?”
  6. “또 눌렀네요. 이유가 있나요?”
  7. “그러다 큰일 납니다(?)”
  8. “눌러보라고 쓴 거 아닙니다.”
  9. “이건 테스트가 아니에요.”
  10. “정말 마지막 경고입니다(아마도).”
  11. “손가락을 잠시 쉬게 하세요.”
  12. “그 호기심, 위험합니다.”
  13. “버튼과 거리두기 해요.”
  14. “클릭 자제 부탁드립니다.”
  15. “버튼이 슬퍼합니다.”
  16. “당신의 인내심을 믿습니다.”
  17. “이쯤이면 멈춰도 되죠?”
  18. “다음 클릭은 비추천입니다.”
  19. “정말 정말 누르지 마세요.”
  20. “여기까지 온 건 비밀로 하죠.”

**FR-4. 10번째 클릭 시 결제 확인 모달**

* 클릭 카운트가 **정확히 10**이 되는 시점에 모달 표시:

  * 메시지(영어): **"Would you like to proceed with payment?"**
  * 버튼: **Yes**, **No**

**FR-5. 모달 선택 동작**

* **Yes** 클릭 → 팝업/알림으로 **"Payment completed"** 표시 (닫으면 원래 화면 유지)
* **No** 클릭 → 아무 변화 없음(모달만 닫힘, 카운트/상태 그대로)

**FR-6. 카운트 유지 정책 (MVP)**

* 새로고침 시 카운트는 **초기화**(세션 보존 없음).

  * (vNext 옵션: `localStorage`로 유지 가능)

---

## D. 비기능 요구사항(Non-Functional Requirements, NFR)

**NFR-1. 성능**: 클릭 상호작용은 100ms 내 UI 반응.
**NFR-2. 접근성(A11y)**:

* 버튼은 키보드 포커스 가능(Tab), Enter/Space로 활성화 가능.
* 모달은 표시 시 포커스 트랩, ESC로 닫기 가능.
  **NFR-3. 반응형**: 360px 모바일 화면에서도 깨짐 없이 레이아웃 유지.
  **NFR-4. 브라우저 호환**: 최신 Chrome/Safari/Edge 지원.
  **NFR-5. 스타일**: “조악한” 느낌을 위해 의도적 폰트/텍스트 쉐도우/약간의 왜곡(과도하지 않게).
  **NFR-6. 보안/프라이버시**: 외부 전송 데이터 없음. 쿠키/추적 없음.
  **NFR-7. 배포 용이성**: 정적 호스팅 1파일(HTML/CSS/JS) 또는 단일 번들로 제공.

---

## E. 상태 모델(State Model)

* **Idle**(초기) — `count=0`
* **Counting** — `0 < count < 10`, 각 클릭마다 랜덤 문구 갱신
* **Confirming** — `count == 10`, 결제 확인 모달 표시
* **Completed** — Yes 선택 직후 “Payment completed” 팝업 표시(종료 후 Counting으로 복귀, count는 10 유지 또는 0으로 리셋 여부는 MVP에선 **유지**: 후속 클릭 시 추가 모달 없는 단순 카운팅 상태)

> 결정: MVP에서는 **10 이후 클릭에도 추가 모달 없음**(간단성 유지).
> (vNext: 10의 배수마다 모달 재등장 옵션)

---

## F. 이벤트/동작 정의

* **EVT\_CLICK\_BUTTON**:

  * `count++`
  * 경고 문구 랜덤 표기
  * `if count == 10` → `MODAL_OPEN(CONFIRM_PAYMENT)`
* **EVT\_MODAL\_YES**: `ALERT("Payment completed")` → 모달 닫기
* **EVT\_MODAL\_NO**: 모달 닫기(상태 변화 없음)

---

## G. 데이터 모델(Data Model)

```json
{
  "clickCount": 0,
  "randomMessages": [
    "분명 누르지 말랬죠?",
    "왜 누르셨나요…?",
    "다음엔 참아볼까요?",
    "진짜 누르지 말랬는데요.",
    "혹시 경고를 못 보신 건가요?",
    "또 눌렀네요. 이유가 있나요?",
    "그러다 큰일 납니다(?)",
    "눌러보라고 쓴 거 아닙니다.",
    "이건 테스트가 아니에요.",
    "정말 마지막 경고입니다(아마도).",
    "손가락을 잠시 쉬게 하세요.",
    "그 호기심, 위험합니다.",
    "버튼과 거리두기 해요.",
    "클릭 자제 부탁드립니다.",
    "버튼이 슬퍼합니다.",
    "당신의 인내심을 믿습니다.",
    "이쯤이면 멈춰도 되죠?",
    "다음 클릭은 비추천입니다.",
    "정말 정말 누르지 마세요.",
    "여기까지 온 건 비밀로 하죠."
  ],
  "uiText": {
    "header": "Don't Press Button",
    "button": "Don't Press Button",
    "confirmPaymentTitle": "Would you like to proceed with payment?",
    "confirmYes": "Yes",
    "confirmNo": "No",
    "paymentCompleted": "Payment completed"
  }
}
```

---

## H. 설정 파일(app.config.json) 스키마

```json
{
  "pressToConfirmCount": 10,
  "persistCount": false,
  "messages": "@use: DataModel.randomMessages",
  "uiText": "@use: DataModel.uiText",
  "a11y": {
    "trapFocusInModal": true,
    "closeOnEsc": true
  }
}
```

---

## I. 수용 기준(Acceptance Criteria)

* **AC-1**: 페이지 로드시 상단에 “Don't Press Button” 텍스트가 보인다.
* **AC-2**: 빨간 버튼 클릭 시 카운트가 1씩 증가하고 버튼 **윗 공간**의 문구가 매번 랜덤 교체된다.
* **AC-3**: 정확히 **10번째** 클릭 시 결제 확인 모달이 열리고, 영어 문구/Yes/No가 표시된다.
* **AC-4**: 모달에서 **Yes** → “Payment completed” 팝업이 즉시 뜬다.
* **AC-5**: 모달에서 **No** → 아무 변화 없이 모달만 닫힌다.
* **AC-6**: 새로고침하면 카운트는 0으로 초기화된다(`persistCount=false`).
* **AC-7**: 모바일(360px 폭)에서도 버튼·문구·모달이 깨짐 없이 보인다.
* **AC-8**: 키보드로 버튼 활성화/모달 포커스 트랩/ESC 닫기가 동작한다.

---

## J. 테스트 시나리오(Gherkin)

```gherkin
Feature: Don't Press Button micro app

  Scenario: Initial render
    Given I open the app
    Then I should see text "Don't Press Button" above a red button labeled "Don't Press Button"

  Scenario: Random scolding on each click
    Given clickCount is 0
    When I click the red button
    Then clickCount becomes 1
    And a Korean scolding message appears above the button
    When I click the red button again
    Then clickCount becomes 2
    And a (potentially different) scolding message appears

  Scenario: Payment confirmation on 10th click
    Given clickCount is 9
    When I click the red button
    Then a modal appears with "Would you like to proceed with payment?"
    And the modal shows buttons "Yes" and "No"

  Scenario: Confirm payment (Yes)
    Given the confirmation modal is open
    When I click "Yes"
    Then I should see an alert "Payment completed"
    And the modal closes

  Scenario: Decline payment (No)
    Given the confirmation modal is open
    When I click "No"
    Then no alert appears
    And the modal closes
    And clickCount remains 10

  Scenario: Refresh resets count (MVP)
    Given clickCount is 5
    When I refresh the page
    Then clickCount is 0
```

---

## K. UoW(작업 단위) 분해

* **UoW-001: 기본 골격/레이아웃**

  * 헤더 텍스트, 빨간 버튼, 메시지 표시 영역 DOM 구성
  * 최소 스타일(모바일 대응)

* **UoW-002: 상태·이벤트 로직**

  * `clickCount` 상태, 클릭 핸들러
  * 랜덤 메시지 선택, 영역 갱신

* **UoW-003: 결제 확인 모달**

  * 모달 컴포넌트/표시 토글
  * A11y: 포커스 트랩/ESC 닫기

* **UoW-004: Yes/No 동작**

  * Yes → alert “Payment completed”
  * No → no-op + 모달 닫기

* **UoW-005: 설정 주입**

  * `app.config.json` 로딩(혹은 빌드 시 인라인)
  * `pressToConfirmCount`, `persistCount` 반영

* **UoW-006: 테스트/검수**

  * 수동 테스트 케이스 실행(Gherkin 기준)
  * 간단한 E2E 스모크(Playwright/Cypress 선택사항)

---

## L. 에지 케이스/결정

* 10번째에서만 모달 → **그 이후(11, 12…)에는 모달 없음**(MVP 단순화).
* 브라우저 탭 숨김/복원과 무관하게 상태 유지(세션 내).
* 다국어 확장(EN/KR i18n)은 **vNext**.

---

## M. 모니터링/로그(선택)

* 콘솔 로그(개발 모드): 클릭 횟수, 모달 오픈/선택 이벤트.
* 프로덕션: 없음(MVP 단순성 유지).

---

## N. 배포(Deployment)

* 정적 호스팅만으로 배포 가능(단일 HTML 파일 또는 Vite/CRA 번들).
* 캐시-컨트롤: `no-cache` 권장(문구 실험 시 즉시 반영).

---

## O. vNext 제안(선택)

* 10의 배수마다 모달 재등장 옵션
* `localStorage` 기반 카운트 유지
* i18n(EN/KR 토글)
* 실험용 A/B 문구 풀 관리(노출·반응 로깅)

---

## P. 미니 UI 가이드(요약)

* 헤더: 상단 중앙, 거친 폰트/텍스트 쉐도우로 “조악한 느낌” 표현
* 메시지 영역: 헤더와 버튼 사이(버튼 **위**), 1\~2줄 고정 높이
* 버튼: 크고 두툼한 **빨간색**, 호버 시 진한 레드, 포커스 링 선명

---

## Q. 변경관리·리스크

* **변경점**: 모달 트리거 임계치, 문구 리스트, 카운트 지속 여부
* **리스크**: 조악 스타일이 UX/접근성 저하로 느껴질 수 있음 → 대비: 대비·포커스 링 명확화

---

## 부록: 빠른 시작용 HTML 스켈레톤(선택, 주석은 영어)

> **참고**: 구현 요청 시 프레임워크(React/Vanilla) 버전으로 정리하여 전달드립니다.

```html
<!-- Minimal skeleton for MVP demo; production build should split CSS/JS -->
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Don't Press Button</title>
  <style>
    /* Intentional "rough" header styling */
    body{font-family:system-ui,Arial,sans-serif;display:flex;min-height:100vh;margin:0}
    .wrap{margin:auto;text-align:center;max-width:520px;padding:16px}
    h1{font-size:28px;letter-spacing:0.5px;text-shadow:1px 1px 0 #0002, -1px -1px 0 #0001;transform:skewX(-2deg)}
    #msg{min-height:2.2em;margin:12px 0 20px;font-size:16px}
    button{background:#d62828;color:#fff;border:none;border-radius:10px;padding:16px 24px;font-size:18px;cursor:pointer}
    button:hover{filter:brightness(0.95)}
    button:focus-visible{outline:3px solid #000}
    dialog{border:none;border-radius:12px;box-shadow:0 10px 30px #0004;padding:20px}
    .row{display:flex;gap:10px;justify-content:center;margin-top:10px}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Don't Press Button</h1>
    <div id="msg"></div>
    <button id="btn">Don't Press Button</button>
    <dialog id="confirm">
      <div>Would you like to proceed with payment?</div>
      <div class="row">
        <button id="yes">Yes</button>
        <button id="no">No</button>
      </div>
    </dialog>
  </div>
  <script>
    // State & messages (MVP, no persistence)
    const messages = [
      "분명 누르지 말랬죠?","왜 누르셨나요…?","다음엔 참아볼까요?","진짜 누르지 말랬는데요.",
      "혹시 경고를 못 보신 건가요?","또 눌렀네요. 이유가 있나요?","그러다 큰일 납니다(?)","눌러보라고 쓴 거 아닙니다.",
      "이건 테스트가 아니에요.","정말 마지막 경고입니다(아마도).","손가락을 잠시 쉬게 하세요.","그 호기심, 위험합니다.",
      "버튼과 거리두기 해요.","클릭 자제 부탁드립니다.","버튼이 슬퍼합니다.","당신의 인내심을 믿습니다.",
      "이쯤이면 멈춰도 되죠?","다음 클릭은 비추천입니다.","정말 정말 누르지 마세요.","여기까지 온 건 비밀로 하죠."
    ];
    let count = 0;
    const btn = document.getElementById("btn");
    const msg = document.getElementById("msg");
    const dlg = document.getElementById("confirm");
    const yes = document.getElementById("yes");
    const no  = document.getElementById("no");

    // Update scolding message
    function updateMessage() {
      const pick = messages[Math.floor(Math.random()*messages.length)];
      msg.textContent = pick;
    }

    // Button click handler
    btn.addEventListener("click", () => {
      count += 1;
      updateMessage();
      if (count === 10) {
        dlg.showModal(); // A11y note: focus is trapped by default in dialog
      }
    });

    // Modal actions
    yes.addEventListener("click", () => {
      alert("Payment completed");
      dlg.close();
    });
    no.addEventListener("click", () => {
      dlg.close(); // do nothing else
    });

    // ESC closes dialog (native)
  </script>
</body>
</html>
```