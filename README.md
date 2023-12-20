# Kulkan's CTF challenge for Ekoparty 2023 (https://www.ekoparty.org)

## Building the CTF challenge

docker build --tag eko-ctf-kulkan-2023 .

## Running the CTF challenge as a single container and plaintext HTTP

docker run -p12000:12000 eko-ctf-kulkan-2023

## Solving the CTF challenge

No spoilers.

## Scaling the CTF Challenge and adding LetsEncrypt HTTPS

### stack

- Dockerized Flask app & Admin bot python apps
- ngnix with rate limiting rules listening both on 80 and 443
- certbot issuing LetsEncrypt certificates for the virtualhost served by nginx
- Docker swarm managing multiple containers

### Prereqs

- Docker installed with Docker compose plugin
- Ensure nginx configuration is set to correct domains
- Ensure you've not skipped calling init-letsencrypt.sh
- Firewall rules open on hosting/cloud provider for ports 80 and 443

### STEPS

- 1) Build the image locally using the steps described above
- 2) Run init-letsencrypt.sh to setup files required for the nginx container to start 
- 3) Run <code> docker stack deploy -c docker-compose.yml eko-ctf-kulkan-2023 </code>
- 4) Run <code> docker node ls</code> to list all running nodes
- 5) Create replicas of desired containers using <code> docker service scale eko-ctf-kulkan-2023-{node-name}={replica_number}</code>

Example: <code> docker service scale eko-ctf-kulkan-2023-ngnix=2 </code>

This creates 2 nginx containers that will automagically load balance between each other

## TODO

- [  ] More aggressive tests to verify availability
- [  ] Ansible script or similar to automate deployment in case main server gets quacked and we need to rehost quickly?

## Kudos

- Matias Forti for creating the challenge and incorporating nginx rate limits
- Philipp's article on certbot+nginx integration with docker (https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71) and for the creation of init-letsencrypt.sh linked in the article.
