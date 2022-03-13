# AIDUez3.0 <span style="font-size:1.3rem; font-weight:lighter">(Last Updated: 3/14/22)</span>

## Development

- Docker Image 만들기

```console
# 소스 코드 Clone후에 도커 이미지(dev) 빌드
-$ docker build -t (image name) .  
```

- Jupyter Notebook

```console
# Container 실행
-$ docker run -itd -p 8888:8888 -v (source code path for volume mount):/opt/code/aiduez --name (container name) (image name) /bin/bash

# Container 접속 후, Jupyter Notebook 실행
-$ jupyter notebook --ip 0.0.0.0 --notebook-dir /aihub/workspace --allow-root --no-browser

# jupyter 'HomePage'에서 'AIDUez.ipynb' 실행
```
- Voila

<img alt="Run Voila in notebook" src="assets/images/README_voila.png" style="border: 1px solid #eee; border-radius: 4px; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);">

<br>

## Production

- Dspace: Jenkins > Nexus에 이미지 생성 > AIDU repogitory 등록

- OKD Ez실행 yaml에 아래와 같이 적용

```console
source /etc/bash.bashrc && voila /aihub/workspace/AIDUez.ipynb --ip 0.0.0.0 --port 8888 --no-browser
```
<br>

### (Update history)

```console
(3/13/22)
- Tabula AI Training:
  . 훈련 결과 - 차트 부분 추가

- Dokerfile:
  . Dev-Test-Production 하나로 합침
```

```console
(3/8/22)
- notebook 실행 위치 및 tmp 위치 변경: 
  . notebook 실행 위치: /opt/code/aiduez -> /aihub/workspace 
  . tmp 위치: /opt/code/aiduez/tmp -> /aihub/workspace/tmp

- notebook으로 ez3.0 실행하는 방식 변경:
  . 'app.ipynb' 실행 -> javascript로 자동 실행('new'클릭)
```

```console
(3/1/22)
- localhost에서 Jupyter Notebook 접속 에러 나는 현상 발생에 따른 README 수정: 
  . Container 실행 시 '-p 8888:8888' 추가 
  . Jupyter 실행 시 '--ip 0.0.0.0' 추가
```


