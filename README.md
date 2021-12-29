# AIDUez3.0

## Docker Image 만들기

```console
-$ git clone https://github.com/neothology/aiduez_renewal.git
-$ docker build -t (image name) .  
```

## Docker Container 실행

- Jupyter Notebook 자동 실행

```console
-$ docker run -p 8888:8888 (image name)

# Container 실행 후, Browser로 접속
- localhost:8888

# Browser 접속 후, 'app.ipynb' 실행 또는 Notebook 에서 아래 코드 실행
> from app import Aian
> aian = Aian()
> aian.start()
```

- Container 접속하여 Jupyter Notebook 수동 실행 (Volume mount로 소스 코드 실행)

```console
-$  docker run -itd -v (source code path for volume mount):/opt/code --name (container name) (image name) /bin/bash

# Container 접속 후, Jupyter Notebook 실행
-$ cd /opt/code
-$ jupyter notebook --allow-root

# Browser 접속 후, 'app.ipynb' 실행 또는 Notebook 에서 아래 코드 실행
> from app import Aian
> aian = Aian()
> aian.start()
```
