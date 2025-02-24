# Kubernetes Cluster with Bitcoin Price Fetcher
## Kubernetes cluster setup using AKS-Engine, including services, deployments, and ingress configuration.

This repository contains the code and configuration to set up a production-ready Kubernetes cluster on Azure using AKS-Engine. The cluster is built from scratch (without using pre-defined AKS solutions).

## Project Overview

- **Cluster Setup:**
  The project deploys a Kubernetes cluster on Azure using AKS-Engine.

- **Services:**
  The cluster consists of two primary services:
  - **Service A:**
    The Bitcoin price fetcher application queries the CoinGecko API every minute to obtain the current Bitcoin price in USD and prints the result. Additionally, every 10 minutes, it calculates and displays the average price over that interval.
  - **Service B:**
    A standalone service that is isolated from Service A, is used to demonstrate network isolation. Network policies are in place to prevent Service A from communicating with Service B.

- **Ingress Controller:**
  An Ingress controller is configured to route external traffic based on URL paths. Requests to `xxx/service-A` or `xxx/service-B` are directed to the respective services.

- **Production-Ready Practices:**
  The deployment is automated and fully repeatable using YAML templates. Each Pod is equipped with liveness and readiness probes to ensure high availability and self-healing.

## Repository Structure

- **`deployment.yaml`** – Deployment configuration for the Bitcoin price fetcher application.
- **`service-a.yaml`** – Service definition for Service A.
- **`service-b.yaml`** – Service definition for Service B.
- **`Dockerfile`** – Docker build file for packaging the Bitcoin price fetcher.
- **`bitcoin_price_fetcher.py`** – Python application script for Service A that fetches and processes Bitcoin price data.
- **`requirements.txt`** - A requirements file for the Python script.

## Troubleshooting the CoreDNS API Connection Issue

While setting up the cluster, I observed this CoreDNS warning:
> [WARNING] plugin/kubernetes: Kubernetes API connection failure: Get "https://10.0.0.1:443/version": dial tcp 10.0.0.1:443: connect: no route to host

This warning indicates that CoreDNS was unable to connect to the Kubernetes API server, suggesting that the service isn’t operational. As a result, the pod cannot resolve external resources like the Bitcoin API, leading to errors such as:
> Failed to resolve 'api.coingecko.com'


### What I Tried and Lessons Learned

- **Pod-Level Diagnostics & Network Testing** - I accessed the CoreDNS pod’s environment and ran a series of network connectivity tests to verify whether the expected route to the Kubernetes API server was available. These tests confirmed that the necessary network path was missing, indicating a configuration issue.

- **Reviewing DNS Configurations** - As part of my troubleshooting process, I modified the DNS configuration for the application pods by disabling the default DNS policy and specifying external nameservers. This change was an attempt to bypass CoreDNS and force external DNS resolution temporarily. However, this workaround did not restore connectivity, confirming that the root cause lay elsewhere.

- **Additional Diagnostic Measures** - I also launched a dedicated debug pod and used its terminal to perform hands-on troubleshooting. By manually issuing network tests and trying alternative DNS resolution methods from within the debug environment, I aimed to circumvent the issue. Despite these efforts, the problem persisted.

This debugging process enhanced my understanding of Kubernetes networking and DNS configurations. It proved to be a valuable exercise in troubleshooting production systems.

## Ingress Controller (NGINX) – Deployment Limitation

The deployment of the NGINX Ingress Controller encountered the same ***No Route to Host*** issue that affected CoreDNS. This prevented the ingress controller from successfully starting, making it non-functional in the cluster.

### Intended Implementation

Had the network issue not been present, the Ingress Controller would have been implemented following the guidance from the [AKS-Engine AzureStack documentation](https://github.com/Azure/aks-engine-azurestack/blob/master/docs/howto/mixed-cluster-ingress.md). While the documentation assumes a mixed (Linux + Windows) node setup, I would have adapted the process to a Linux-only environment to match the cluster configuration.

Despite the failure, I created the necessary [YAML configuration](https://github.com/NirKors/aks-engine-cluster/blob/main/YAML/ingress.yaml) for the Ingress resource, which outlines how traffic would have been routed if the Ingress Controller had functioned correctly.

## Next Steps
Once the ***No Route to Host*** is addressed, CoreDNS will be able to connect to the Kubernetes API server, ensuring proper DNS resolution.

As a result, the Bitcoin price fetcher script should reliably access external APIs, and the NGINX Ingress Controller will route traffic correctly.
With all YAML configurations pre-prepared, a simple `kubectl apply` will deploy and activate the complete, production-ready cluster setup.
