# Pull base image
FROM python:3.8

# RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
# && apt-get clean \
# && apt-get update \
# && apt-get install -y libgl1-mesa-glx
# RUN apt-get update


# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set requirements
ARG requirements=requirements/production.txt

# Set work directory
WORKDIR /django-project-lite/code

# Install dependencies
COPY requirements/ /django-project-lite/code/requirements/
RUN pip install --default-timeout=1000 --ignore-installed -i https://pypi.tuna.tsinghua.edu.cn/simple -r $requirements

# Copy project
COPY . /django-project-lite/code/

