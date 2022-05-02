# AIDUez3.0 <span style="font-size:1.3rem; font-weight:lighter">(Last Updated: 4/28/22 - 00:58AM)</span>

## Development

- Docker Image 만들기

```console
# 소스 코드 Clone후에 도커 이미지 빌드
-$ docker build -t (image name) .  
```

- Jupyter Notebook으로 개발

```console
# Container 실행
-$ docker run -itd -p 8888:8888 -v (source code path for volume mount):/opt/code/aiduez --name (container name) (image name) /bin/bash

# Container 접속 후, Jupyter Notebook 실행
-$ jupyter notebook --ip 0.0.0.0 --notebook-dir /aihub/workspace --allow-root --no-browser --base_url /test/

# jupyter 'HomePage'에서 'AIDUez.ipynb' 실행
```
- Voila 결과 확인
```console
-$ source /etc/bash.bashrc && voila /aihub/workspace/AIDUez.ipynb --ip 0.0.0.0 --port 8888 --no-browser --enable_nbextensions True --base_url /test/
```