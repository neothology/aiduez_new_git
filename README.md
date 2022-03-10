# AIDUez3.0 <span style="font-size:1.3rem; font-weight:lighter">(Last Updated: 3/8/22)</span>

## Development <span style="font-size:1.2rem; font-weight:lighter">(local에서 개발)</span>

- Docker Image 만들기

```console
# 소스 코드 Clone후에 도커 이미지(dev) 빌드
-$ docker build -t (image name) -f Dockerfile_dev .  
```

- Jupyter Notebook

```console
# Container 실행
-$ docker run -itd -p 8888:8888 -v (source code path for volume mount):/opt/code/aiduez --name (container name) (image name) /bin/bash


# Container 접속 후, Jupyter Notebook 실행
-$ cd /opt/code/aiduez
-$ jupyter notebook --ip 0.0.0.0 --allow-root

# jupyter 'HomePage'에서 'app.ipynb' 실행
```

- Voila

 <img alt="Run Voila in notebook" src="assets/images/README_voila.png" style="border: 1px solid #eee; border-radius: 4px; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);">

## Test <span style="font-size:1.2rem; font-weight:lighter">(AIDU에 올리고 Jupyter Notebook으로 실행)</span>

- "dockerfile_test" 사용해서 Dspace-Nexus에 이미지 생성 > aidu repogitory 등록

- 기존 ez yaml 변경 없이 실행

```console
voila /opt/code/aiduez/app.ipynb --no-browser --ip 0.0.0.0 
```

## Production <span style="font-size:1.2rem; font-weight:lighter">(AIDU에 올리고 Voila로 실행)</span>

- "dockerfile_prod" 사용해서 Dspace-Nexus에 이미지 생성 > aidu repogitory 등록

- OKD Ez실행 yaml에 아래와 같이 적용

```console
voila /opt/code/aiduez/app.ipynb --no-browser --ip 0.0.0.0 
```

## *Update history

```console
(3/8/22)
- XXX: 
  . XXX 
```

```console
(3/1/22)
- localhost에서 Jupyter Notebook 접속 에러 나는 현상 발생에 따른 README 수정: 
  . Container 실행 시 '-p 8888:8888' 추가 
  . Jupyter 실행 시 '--ip 0.0.0.0' 추가
```

