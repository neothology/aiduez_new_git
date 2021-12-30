# AIDUez3.0

## Docker Image 만들기

```console
-$ git clone https://github.com/neothology/aiduez_renewal.git
-$ docker build -t (image name) .  
```

## Docker Container & Jupyter notebook 실행

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

## Voila 실행

- (방법1) Jupyter Notebook 내에서 실행 (메뉴 -> Voila 버튼 클릭)

 <img alt="Run Voila in notebook" src="assets/images/README_voila.png" style="border: 1px solid #eee; border-radius: 4px; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);">

- (방법2) Jupyter Notebook 실행 후, browser 노트북 주소에 추가/수정하여 voila 실행

```console
# (host url) /voila/render/ (notebook name)
(예시) http://localhost:8888/voila/render/app.ipynb
```

- (방법3) Jupyter Notebook 실행하지 않고 Voila 단독 실행

```console
# 특정 Notebook 직접 실행 하는 경우
-$ voila (notebook path)
- Browser > localhost:8866 으로 접속
```

```console
# voila 실행 후, browser의 notebook 주소 통해 접근하는 경우
-$ voila
- Browser > localhost:8866/voila/render/(notebook name) 으로 접속
(예시) http://localhost:8866/voila/render/app.ipynb

```