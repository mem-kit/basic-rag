
## Build

https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

```
	python3 -m venv .venv

	source .venv/bin/activate

	python3 -m pip install -r requirements.txt

	which python
	
	which python3
```

## Run

please check the start.sh script run it with **root** to open the 80 port in linux kernel. 
With ``` sudo -i ```

ohup streamlit run streamlit_app.py --server.port 18880 &

## Docker 

docker build -t streamlit-app:1.0.0 .

docker run -d -p 18880:18880 --name rai-app streamlit-app:1.0.0
