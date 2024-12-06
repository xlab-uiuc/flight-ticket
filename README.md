# The FlightTicket Serverless Application Benchmark

FlightTicket is a serverless application benchmark running on top of [OpenWhisk](https://openwhisk.apache.org/) on [Kubernetes](https://kubernetes.io/). 
The application is architectured based on the [AirplaneTicket](https://github.com/FudanSELab/airplane-ticket) benchmark. 
Different from AirplaneTicket, FlightTicket is implemented in Python and runs as a serverless application on [OpenWhisk](https://openwhisk.apache.org/).

One key feature of FlightTicket is that, instead of using a synthetic input generator, FlightTicket uses the [US-airlines dataset](https://osf.io/6398x/) from the US Department of transport.

FlightTicket is created by [Jovan Stojkovic](https://jovans2.github.io) and is maintained by [Alan Andrade](https://github.com/Alan-S-Andrade). 

## Use the FlightTicket benchmark

Deploy a minikube cluster
```
minikube start --cpus=8
```

### Deploy OpenWhisk
Install and initialize helm for deploying openwhisk
```
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

Init helm and install Tiller to the K8 cluster
```
helm init
kubectl create clusterrolebinding tiller-cluster-admin --clusterrole=cluster-admin --serviceaccount=kube-system:default
```

Install and Deploy OpenWhisk, grab the cluster's internal IP to add to the openwhisk deploy `mycluster.yaml` config file.
```
git clone https://github.com/apache/openwhisk-deploy-kube.git
cd openwhisk-deploy-kube
minikube ip # add use this to edit mycluster.yaml
vim deploy/kind/mycluster.yaml # edit apiHostName to be the x.x.x.x IP from last cmd e.g. apiHostName = 192.168.49.2
```

Edit the values.yaml config file to allow more than 60 function invocations per minute:
```
vim helm/openwhisk/values.yaml
set both of these to 1000:
    actionsInvokesPerminute: 1000
    actionsInvokesConcurrent: 1000
```
Now we are ready to deploy OpenWhisk
```
helm install owdev ./helm/openwhisk -n openwhisk --create-namespace -f ./deploy/kind/mycluster.yaml # we use this mycluster.yaml as it has single-node config
```

Watch OpenWhisk deployment, wait for **owdev-install-packages** to be **Completed** meaning OW was deployed successfully. Should take around 10 min.
```
kubectl get pods -n openwhisk --watch
```

Run these commands to use the wsk CLI on your openwhisk namespace
```
wget https://github.com/apache/openwhisk-cli/releases/download/1.2.0/OpenWhisk_CLI-1.2.0-linux-amd64.tgz
tar -zxvf OpenWhisk_CLI-1.2.0-linux-amd64.tgz
chmod +x wsk
sudo mv wsk /usr/bin/
wsk property set --apihost <whisk.ingress.apiHostName>:<whisk.ingress.apiHostPort>
wsk property set --auth 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP
```

### Deploy FlightTicket

```
cd flight-ticket
vim QueryForTravel/__main__.py # edit APIHOST as described above
(do this for the rest of the functions)
```

Unzip it under the root folder:

```shell
unzip clean.zip -d clean
```

Download flight ticket data from OSF:
https://files.osf.io/v1/resources/6398x/providers/osfstorage/5ff8362686541a012814b8a4/?zip=

Next, build and push docker images, deploy functions as OpenWhisk actions then create sequence (workflow).
Also, we need to deploy Redis and populate it with AirplaneTicket data (only to be done once):
```
sudo apt update
sudo apt install redis-server
sudo service redis-server start
pip install redis
./deploy_ow_actions.sh
```

Run workflow with eventing:
```
python3 run-all.py --minutes <workflow_duration>
```
