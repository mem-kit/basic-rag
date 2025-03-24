#!/bin/sh

export PYTHONPATH="/app:{PYTHONPATH}"

# GUI Web App
nohup streamlit run streamlit_app.py \
  --server.baseUrlPath=$BASE_URL_PATH_WEB \
  --server.port 18880 \
  --server.address 0.0.0.0 \
  /dev/null 2>&1 &

# Stay until background process exit
wait