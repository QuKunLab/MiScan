FROM python:3.7
LABEL author='jeffery' email='jeffery_cpu@163.com'
ENV requirements="requirements.txt" wd="/miscan" \
DEBIAN_FRONTEND="noninteractive"
WORKDIR $wd
COPY './' $wd
RUN apt-get update && apt-get install --assume-yes apt-utils && \
apt-get -y --allow-unauthenticated --assume-yes upgrade
RUN apt-get install bedtools && apt-get autoremove
RUN pip install --upgrade pip && pip install -r $requirements && python3 setup.py sdist bdist_wheel && \
ls dist/*whl | xargs pip install  && rm -r ~/.cache/pip && rm -rf ./*
ENTRYPOINT ["MiScan"]