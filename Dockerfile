FROM public.ecr.aws/docker/library/python:3.7-alpine3.16

COPY . . 

RUN pip install -r requirements.txt

EXPOSE 80 
CMD ["python", "./server.py"]