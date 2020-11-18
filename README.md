# oauth-plugin-api

## Project plan
- 간단하게 작동하는 oauth server륾 만들고 싶다.
- 작동 환경은 aws lambda에서 동작 할 수 있게 chalice를 이용해서 배포할 생각이다.
- DB는 주소를 입력하거나, 없을 시에 새롭게 생성을 한다..
    - nosql과 RDB를 지원하게 만든다..
    - 람다에서 sqlAlcemy를 사용할 수 있나 찾아보자
- 다른 라이브 러리들을 확인해보니까 email을 이용해서 인증을 받던데 정확한 방식을 이해하자.
## 20.11.18 Issue
- chalice 환경을 생각해보니 session을 유지할 수 없는 환경이다.
    session을 유지할 수 없어서 지금 동작 방식으로는 한계가 있을것이라 생각이 된다.
    차선책으로 aws cognito를 이용해서 oauth를 동작 할 수 있다.
    찾아보니 aws 개발자가 만든 라이브러리가 존재한다..
    Docker를 사용하는 프로잭트로 변경해야하나 고민이된다.
