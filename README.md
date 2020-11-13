# oauth-plugin-api

## Project plan
- 간단하게 작동하는 oauth server륾 만들고 싶다.
- 작동 환경은 aws lambda에서 동작 할 수 있게 chalice를 이용해서 배포할 생각이다.
- DB는 주소를 입력하거나, 없을 시에 새롭게 생성을 한다..
    - nosql과 RDB를 지원하게 만든다..
    - 람다에서 sqlAlcemy를 사용할 수 있나 찾아보자
- 다른 라이브 러리들을 확인해보니까 email을 이용해서 인증을 받던데 정확한 방식을 이해하자.