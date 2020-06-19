# A Deed Poll Generator Written in Python Flask

The site live [here](http://deedpoll.mavieson.co.uk/)

Prerequisites: [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

To run:

```bash
docker pull mavi0/deedpolgenerator
docker run --name deedpolgenerator -d -p 5000:5000 mavi0/deedpolgenerator:latest
```

Docker compose with traefik
```yaml
deedpol:
    image: mavi0/deedpolgenerator:latest
    container_name: deedpol
    networks:
      - traefik-network
      - default
    environment:
      - PUID=${PUID}
      - PGID=${PGID}
      - TZ=${TZ}
    restart: unless-stopped
    labels:
      - traefik.enable=true
      - traefik.http.routers.deedpol.entrypoints=web
      - traefik.http.routers.deedpol-sec.entrypoints=websecure
      - traefik.http.routers.deedpol.rule=Host(`deedpoll.mavieson.co.uk`)
      - traefik.http.routers.deedpol-sec.rule=Host(`deedpoll.mavieson.co.uk`)
      - traefik.http.services.deedpol-sec.loadbalancer.server.port=5000
      - traefik.http.routers.deedpol.middlewares=basic-http
      - traefik.http.routers.deedpol-sec.middlewares=basic
      - traefik.http.routers.deedpol-sec.tls=true
      - traefik.http.routers.deedpol-sec.tls.certresolver=cfdns

networks:
  traefik-network:
    external: true
  default:
    driver: bridge
```

Goto [127.0.0.1:5000](http://127.0.0.1:5000)

This project uses Latex files from [this](https://github.com/mavi0/deedpol-template) repo.

## Todo: 

- [ ] Add text explaining how to use the generator - witness req.
- [ ] Add multiple types of deedpol - 1 witness, 2 witness,, fill witness or blank witnesses
- [ ] For GIC, date on deedpol is used as start date of RLE. Requires 2 witnesses. 



## How to fill out this form

There are four options to choose from to generate  your deedpol. You have the option for a one witness or two witness deedpol and you can either prefill the witness details or fill them in at a later date. There is no legal requirement for more than one witness, it is only required in niche cases. There is also the option to change your title. 

A witness must be someone who you know personally, is not related to you, who you have known for at least 2 years and does not live at the same address as you. 

If you are transgender, the GIC will use the date on the deedpol as the start date of "Real Life Experience". The GIC is one of the only institutions who will require two witnesses. A title is simply an honorific and there is no legal process to change it. Companies and government agancies are required under the Equality act and GDPR to update your title on request. 


## For blank witness pages
To fill in the witness(es) at a later date the first line must contain the full name of the witness, the second, third and fourth line must contain the address and the final line must contain their signature.
