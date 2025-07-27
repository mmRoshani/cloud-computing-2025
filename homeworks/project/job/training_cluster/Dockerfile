FROM rayproject/ray:latest

RUN pip install torch torchvision ray[train] boto3 flask

COPY ray_status_server.py /ray_status_server.py

CMD ["bash", "-c", "ray start --head --dashboard-host 0.0.0.0 --dashboard-port 8265 --block & python /ray_status_server.py"]