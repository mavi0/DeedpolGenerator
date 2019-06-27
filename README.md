# A Deedpol Generator Written in Python Flask

The site live [here](http://deedpol.mavieson.co.uk/)

Prerequisites: [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

To run:

```bash
docker pull mavi0/deedpolgenerator
docker run --name deedpolgenerator -d -p 5000:5000 mavi0/deedpolgenerator:latest
```
Goto [127.0.0.1:5000](http://127.0.0.1:5000)

This project uses Latex files from [this](https://github.com/mavi0/deedpol-template) repo.
