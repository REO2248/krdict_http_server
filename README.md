# krdict_http_server
조선말사전파일을 열람하기 위한 봉사프로그람입니다.


아래 파일을 준비하여주십시오

- `KDictionary.db` (사전파일)
- `fonts/PICK D Text.ttf` (서체파일)
- `fonts/PICK Gothic Light.ttf` (서체파일)
- `fonts/PICK Gothic.ttf` (서체파일)
- `fonts/PICK HwanChong.ttf` (서체파일)
- `fonts/PICK Text Black.ttf` (서체파일)
- `fonts/PRK CheonRiMa Long B.ttf` (서체파일)
- `fonts/PRK P Chongbong.ttf` (서체파일)
- `images/image-[수자].png`(사진파일들)

아래 항목을 환경변수(.env)파일에 적어주십시오
- `DICT_PATH` KDictionary.db경로
- `FONTS_PATH` 서체파일들이 있는 서류철 경로
- `IMAGES_PATH` 사진파일들이 있는 서류철 경로
- `USER_NAME` 봉사를 리용할 위한 사용자이름
- `PASSWORD` 봉사를 리용할 위한 통과암호
- `SECRET_KEY` 비밀열쇠 문자렬
- `HOST` 기본적으로 0.0.0.0으로 설정합시다
- `PORT` 봉사가 공개되는 포구번호
- `DEBUG` Flask의 개발자용 설정

