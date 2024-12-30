# The FlightTicket Serverless Application Benchmark

FlightTicket is a serverless application benchmark running on top of [OpenWhisk](https://openwhisk.apache.org/) on [Kubernetes](https://kubernetes.io/). 
The application is architectured based on the [AirplaneTicket](https://github.com/FudanSELab/airplane-ticket) benchmark. 
Different from AirplaneTicket, FlightTicket is implemented in Python and runs as a serverless application on [OpenWhisk](https://openwhisk.apache.org/).

One key feature of FlightTicket is that, instead of using a synthetic input generator, FlightTicket uses the [US-airlines dataset](https://osf.io/6398x/) from the US Department of transport.

## Use the FlightTicket benchmark

### Prerequisites
- A kubernetes cluster (could also be minikube) with helm installed

### Deploy OpenWhisk
#### Install OpenEBS

OpenEBS is a prerequisite for deploying OpenWhisk. If OpenEBS is not already installed, you can install it using Helm.
Run the following commands to install OpenEBS and set the default storage class:
```
helm repo add openebs https://openebs.github.io/charts
helm repo update
helm install openebs openebs/openebs --namespace openebs --create-namespace
kubectl patch storageclass openebs-hostpath -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

Install and initialize helm for deploying openwhisk, follow the [Helm tutorial](https://helm.sh/docs/intro/install/)

Install and Deploy OpenWhisk, grab the cluster's internal IP to add to the openwhisk deploy `mycluster.yaml` config file.
```
git clone https://github.com/apache/openwhisk-deploy-kube.git
cd openwhisk-deploy-kube
```

Get the hostname using `hostname -I` or `minikube ip` if using minikube. Then, edit `deploy/kind/mycluster.yaml` so that `apiHostName` is the proper IP.

run `deploy_wsk.sh` in flight-ticket to allow more than 60 function invocations per minute:
```
./deploy_wsk.sh
```
Now we are ready to deploy OpenWhisk, `cd` back into `openwhisk-deploy-kube` and run the following:
```
helm install owdev ./helm/openwhisk -n openwhisk --create-namespace -f ./deploy/kind/mycluster.yaml
```

Watch OpenWhisk deployment, wait for **owdev-install-packages** to be **Completed** meaning OW was deployed successfully.
```
kubectl get pods -n openwhisk --watch
```

### Deploying flight-ticket
Now, all that's left is to helm install flight-ticket!
```
helm install flight-ticket ./flight-ticket --namespace openwhisk # or any namespace name where openwhisk is installed
```

flight-ticket is ready when the load generator starts running.

## Developing
We have three kubernetes jobs that handle setup and running the load generator:
- `templates/deploy-actions-job.yaml` builds and deploys the OpenWhisk actions
- `templates/populate-redis-job.yaml` downloads the dataset and populates redis
- `templates/load-generator-job.yaml` runs the load generator

There are also a couple of helper jobs that create a service account so that deploy-actions has the permissions it needs for the deployment.

Each of these jobs is a docker image and has it's own directory, `deploy_ow_actions`, `populate_redis`, and `load_generator`. You can rebuild the docker images
using these commands:
```
docker build -t jacksonarthurclark/flight-ticket-load-generator:latest .
docker push jacksonarthurclark/flight-ticket-load-generator:latest
```

Just be sure to update to a dockerhub that you have permissions on, and to update the images used in the helm chart.

### Updating the Helm Chart

If you make changes to the FlightTicket benchmark or its associated jobs, update and publish the Helm chart to reflect those changes. Follow these steps:

1. **Package the Helm Chart**  
   Create a `.tgz` package of the Helm chart:
   ```
   helm package ./flight-ticket
   ```

2. **Switch to the `gh-pages` Branch**  
   Publish the Helm chart by adding it to the `gh-pages` branch of your repository:
   ```
   git checkout gh-pages
   ```

3. **Copy the `.tgz` Package to the `gh-pages` Branch**  
   Move or copy the Helm chart package to the `gh-pages` branch:
   ```
   mv ../flight-ticket-<version>.tgz .
   ```

4. **Generate the `index.yaml` File**  
   Use the Helm CLI to generate or update the `index.yaml` file for the repository:
   ```
   helm repo index . --url https://<your-org>.github.io/flight-ticket
   ```
   Replace `<your-org>` with your GitHub organization or username.

5. **Commit and Push the Changes**  
   Commit the `.tgz` file and the updated `index.yaml` file:
   ```
   git add .
   git commit -m "Update Helm chart for FlightTicket"
   git push origin gh-pages
   ```

6. **Helm Installation Using Published Chart**  
   After publishing, users can install FlightTicket directly from the Helm repository:
   ```
   helm repo add flight-ticket https://<your-org>.github.io/flight-ticket
   helm repo update
   helm install flight-ticket flight-ticket/flight-ticket --namespace openwhisk
   ```
