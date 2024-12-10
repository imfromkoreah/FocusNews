## 🔍📰: 포뉴(FocusNews)

**짧지만 핵심적인 뉴스가 필요해?"**

짧고 간결한 컨텐츠를 소비하는 사회 흐름에 맞춘 뉴스 요약 챗봇입니다!<br>
요약된 핵심 뉴스를 전달해 드릴게요!


---

### 🔔 레포지토리 소개

---

### 🔔 핵심 기술 소개
#### 	1. 네이버 검색 API를 사용한 뉴스 데이터 크롤링

#### 2. OpenAI의 GPT API를 사용한 AI 기반 뉴스 요약 및 분석

#### 3. Karlo API를 이용한 미디어 콘텐츠(카드뉴스) 자동화

---

### 📝 관련링크
	
[Notion](https://www.notion.so/nex2y/88ddd9927caa4a63a7be2c07a7fd74bd?pvs=4) : 공유사항이 적힌 노션<br>
[Pigma](https://www.figma.com/design/1FwURFs3LuHiW3HJ6qjLN1/%ED%8F%AC%EB%89%B4?node-id=0-1&t=rFDal6jrHmIPM73Y-1) : UI 작성

---

### 🖥️ 개발환경

Front : Vue.js<br>
Back : Flask<br>
Server : Github Pages

사용 언어 : Node.js, JS, Python, ...

---

### VSCode에서 프라이빗 Git 리포지토리를 브랜치하여 사용하는 방법을 단계별로 설명드리겠습니다.

### 1. **Git 설치 및 설정**
VSCode에서 Git을 사용하려면 먼저 Git이 로컬 시스템에 설치되어 있어야 합니다. Git이 설치되지 않았다면 [Git 공식 사이트](https://git-scm.com/)에서 설치할 수 있습니다.

1. 설치 후, Git이 제대로 설치되었는지 확인:
   ```bash
   git --version
   ```

2. Git 사용자 정보를 설정합니다:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

### 2. **VSCode에 Git 연동**
VSCode는 Git을 기본으로 지원하지만, 확장 기능을 설치하면 더 편리하게 사용할 수 있습니다.

1. **VSCode 확장 설치**:
   - VSCode의 확장 마켓에서 **GitLens** 확장을 설치하면 Git 히스토리 및 브랜치 관리를 쉽게 할 수 있습니다.

2. **Git 패널 확인**:
   - VSCode 왼쪽 사이드바에서 `Source Control` 아이콘을 클릭하여 Git 패널을 엽니다. 여기에서 리포지토리 상태를 확인할 수 있습니다.

### 3. **프라이빗 리포지토리 클론하기**
먼저, 프라이빗 리포지토리를 클론해와야 합니다. 이를 위해 GitHub, GitLab, Bitbucket 등에서 개인 액세스 토큰을 발급받고, 이를 통해 클론할 수 있습니다.

1. GitHub에서 개인 액세스 토큰 발급:
   - GitHub -> 프로필 -> **Settings** -> **Developer settings** -> **Personal access tokens**로 이동하여 토큰을 생성합니다.
   - 리포지토리에 접근할 수 있도록 권한을 설정합니다.

2. 터미널에서 클론:
   ```bash
   git clone https://github.com/your-username/private-repo.git
   ```
   - URL에 GitHub 사용자 이름과 리포지토리 이름을 입력합니다.
   - 만약 GitHub에서 **SSH**를 사용한다면 SSH 키를 생성하고 사용합니다.

3. 클론 시, 프라이빗 리포지토리 접근을 위해 GitHub 사용자 이름과 비밀번호 또는 **Personal Access Token**을 입력하라는 요청이 뜨면 입력해 주세요.

### 4. **브랜치 생성 및 전환**
프라이빗 리포지토리에서 새로운 브랜치를 만들고 그 브랜치로 전환하는 방법입니다.

1. **새로운 브랜치 생성**:
   ```bash
   git checkout -b feature-branch
   ```
   이 명령은 `feature-branch`라는 새 브랜치를 생성하고 해당 브랜치로 전환합니다.

2. **기존 브랜치 전환**:
   ```bash
   git checkout <branch-name>
   ```
   이 명령은 기존 브랜치로 전환할 때 사용합니다.

3. **브랜치 확인**:
   ```bash
   git branch
   ```
   현재 사용 가능한 브랜치 목록을 보여줍니다. 현재 선택된 브랜치는 `*` 기호가 붙습니다.

### 5. **코드 수정 및 커밋**
VSCode에서 코드를 수정하고 Git을 통해 변경 사항을 커밋하는 방법입니다.

1. **코드 수정**: VSCode에서 코드를 수정합니다.
2. **변경 사항 확인**: `Source Control` 패널에서 수정된 파일을 확인할 수 있습니다.
3. **변경 사항 스테이징**:
   - `Source Control` 패널에서 변경된 파일 옆의 `+` 버튼을 클릭하여 스테이징할 수 있습니다.
   - 또는 터미널에서:
     ```bash
     git add .
     ```
     모든 변경 파일을 스테이징합니다.

4. **커밋**:
   ```bash
   git commit -m "Your commit message"
   ```
   커밋 메시지를 입력하여 변경 사항을 저장합니다.

### 6. **원격 브랜치에 푸시**
새로 생성한 브랜치를 원격 저장소에 푸시하려면 다음 명령을 사용합니다.

```bash
git push origin feature-branch
```
- `feature-branch`는 생성한 브랜치 이름입니다.
- 만약 `git push` 명령을 사용할 때 자격 증명이 필요하다면 GitHub의 개인 액세스 토큰을 사용하여 인증합니다.

### 7. **PR(Pull Request) 생성**
푸시한 브랜치를 GitHub에서 **Pull Request**(PR)로 생성하여 다른 사람과 협업할 수 있습니다.

1. GitHub로 이동하여 해당 리포지토리의 **Pull Requests** 탭으로 가서 새로운 PR을 생성할 수 있습니다.
2. **base** 브랜치와 **compare** 브랜치를 선택한 후, 리뷰어를 지정합니다.

### 8. **Git 상태 및 로그 확인**
- **현재 상태 확인**:
  ```bash
  git status
  ```
  현재 Git 상태를 확인합니다. 어떤 파일이 변경되었는지, 스테이징 상태 등을 보여줍니다.

- **커밋 로그 확인**:
  ```bash
  git log --oneline
  ```
  간략한 커밋 로그를 확인할 수 있습니다.

### 요약
1. Git 및 VSCode 설치.
2. 프라이빗 리포지토리 클론.
3. 새로운 브랜치 생성 및 전환.
4. 코드 수정 후 커밋 및 원격 브랜치 푸시.
5. GitHub에서 PR 생성 및 협업.

이 과정을 통해 프라이빗 리포지토리에서 작업을 브랜치하여 사용할 수 있습니다.