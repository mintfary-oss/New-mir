# Pulumi Examples — Infrastructure as Code

<p align="center">
  <a href="https://www.pulumi.com?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=top-logo" title="Pulumi Examples - Build and Deploy Infrastructure as Code Solutions on Any Cloud">
    <img src="https://www.pulumi.com/images/logo/logo-on-white-box.svg?" width="350">
  </a>
</p>

  [![Slack](http://www.pulumi.com/images/docs/badges/slack.svg)](https://slack.pulumi.com?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=slack-badge)
  [![GitHub Discussions](https://img.shields.io/github/discussions/pulumi/pulumi)](https://github.com/pulumi/pulumi/discussions)
  [![License](https://img.shields.io/github/license/pulumi/pulumi)](LICENSE)

**Pulumi** is the easiest way to build and deploy infrastructure, for any architecture and on any cloud, using programming languages that you already know and love. Code and ship infrastructure faster with your favorite languages and tools, and embed IaC anywhere with [Automation API](https://www.pulumi.com/docs/guides/automation-api/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=about-pulumi).

Pulumi is open source under the [Apache 2.0 license](https://github.com/pulumi/pulumi/blob/master/LICENSE), supports many languages and clouds, and is easy to extend.

## Table of contents

- :rocket: [About This Repo](#about-the-pulumi-examples-repo)
- :toolbox:	[All Pulumi Examples](#all-pulumi-examples)
- :clap: [Contributors](#contributors)
- :busts_in_silhouette: [Pulumi Community](#community)
- :blue_book: [Pulumi Developer Resources](#pulumi-developer-resources)
- :compass:	[Pulumi Roadmap](#pulumi-roadmap)

# About the Pulumi Examples Repo
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/pulumi/examples)

This repository contains examples of using Pulumi to build and deploy cloud applications and infrastructure across major programming languages.

Each example has a two-part prefix, `<cloud>-<language>`, to indicate which `<cloud>` and `<language>` it pertains to. For example, `<cloud>` could be:

- `aws` for [Amazon Web Services](https://github.com/pulumi/pulumi-aws) 
- `azure` for [Microsoft Azure](https://github.com/pulumi/pulumi-azure)
- `gcp` for [Google Cloud Platform](https://github.com/pulumi/pulumi-gcp) 
- `kubernetes` for [Kubernetes](https://github.com/pulumi/pulumi-kubernetes) 

See the [Pulumi documentation](https://www.pulumi.com/docs/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) for more details on getting started with Pulumi.

## Checking out a single example

You can checkout only the example(s) you want by using a [sparse checkout](https://git-scm.com/docs/git-sparse-checkout). The following commands show how checkout only the `aws-go-fargate` example. Replace `aws-go-fargate` with your example of interest.

```bash
$ mkdir examples && cd examples
$ git init
$ git remote add origin -f https://github.com/pulumi/examples/
$ git config core.sparseCheckout true
$ echo "aws-go-fargate" >> .git/info/sparse-checkout ## update this
$ git pull origin master
```

Don't see an example listed? [Try Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) and use natural-language prompts to generate Pulumi infrastructure-as-code programs in _any_ language.

## PR Preview Validation

When making changes to examples, either individual or in bulk, it's useful to validate those changes before submitting a pull request. This repository includes a `make pr_preview` target that provides preview-only sanity checks for changed examples in pull requests. This helps ensure examples remain functional without requiring full deployments.

```bash
# Run preview checks on all changed examples
make pr_preview

# Check what examples would be tested without running previews
DRY_LIST=1 make pr_preview

# Use a custom base branch for comparison
BASE_REF=origin/mybranch make pr_preview
```

The script assumes you have credentials for various providers configured. Examples that fail preview due to missing live resources or complex configuration requirements are expected and don't necessarily indicate problems.

## All Pulumi examples

- [AWS](#aws)
  - [TypeScript](#typescript)
  - [Python](#python)
  - [Go](#go)
  - [C#](#c)
  - [F#](#f)
- [Azure](#azure)
  - [TypeScript](#typescript-1)
  - [Python](#python-1)
  - [Go](#go-1)
  - [C#](#c-1)
  - [F#](#f-1)
- [GCP](#gcp)
  - [TypeScript](#typescript-2)
  - [Python](#python-2)
  - [Go](#go-2)
  - [C#](#c-2)
- [Kubernetes](#kubernetes)
  - [TypeScript](#typescript-3)
  - [Python](#python-3)
  - [Go](#go-3)
  - [C#](#c-3)
- [Openstack](#openstack)
- [OVHCloud](#ovhcloud)
- [DigitalOcean](#digitalocean)
- [Multicloud](#multicloud)
- [F5](#f5)
- [Twilio](#twilio)
- [Linode](#linode)
- [Testing](#testing)
- [Automation API](https://github.com/pulumi/automation-api-examples)

## AWS

### TypeScript

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[API Gateway](aws-ts-apigateway) | Deploy a simple REST API that counts the number of times a route has been hit.
[API Gateway HTTP API with routes](aws-ts-apigatewayv2-http-api) | Deploy a HTTP API that invokes a Lambda.
[API Gateway HTTP API quickstart](aws-ts-apigatewayv2-http-api-quickcreate) | Deploy a very simple HTTP API that invokes a Lambda.
[API Gateway V1 with EventBridge and Lambda](aws-ts-apigateway-eventbridge) | Deploy a REST API that uses EventBridge to target a Lambda function. Includes API Gateway model validation and custom integration-response mapping.
[API Gateway V2 with EventBridge and Lambda](aws-ts-apigatewayv2-eventbridge) | Deploy an HTTP API that uses EventBridge to target a Lambda function.
[Apigateway - Auth0](aws-ts-apigateway-auth0) | Deploy a simple REST API protected by Auth0.
[AppSync](aws-ts-appsync) | Deploy a basic GraphQL endpoint in AWS AppSync.
[AssumeRole](aws-ts-assume-role) | Use AssumeRole to create resources.
[Containers](aws-ts-containers) | Provision containers on Fargate.
[EKS - Dashboard](aws-ts-eks) | Deploy an EKS Kubernetes cluster with an EBS-backed StorageClass, then the Kubernetes Dashboard into the cluster.
[EKS - Hello World](aws-ts-eks-hello-world) | Deploy an EKS Kubernetes cluster with an EBS-backed StorageClass, then a Kubernetes namespace and nginx deployment into the cluster.
[EKS - Migrate Node Groups](aws-ts-eks-migrate-nodegroups) | Create an EKS cluster and node group to use for workload migration with zero downtime.
[Fargate](aws-ts-hello-fargate) | Build, deploy, and run a Dockerized app using ECS, ECR, and Fargate.
[Lambda Thumbnailer](aws-ts-lambda-thumbnailer) | Create a video thumbnail extractor using serverless functions.
[Miniflux](aws-ts-pulumi-miniflux) | Stand up an RSS Service using Fargate and RDS.
[Pulumi Webhooks](aws-ts-pulumi-webhooks) | Create a Pulumi `cloud.HttpEndpoint` that receives webhook events delivered by Pulumi Cloud, then echos the event to Slack.
[RDS and Airflow](aws-ts-airflow) | Deploy a RDS Postgres instance and containerized Airflow.
[Resources](aws-ts-resources) | Create various resources, including `cloudwatch.Dashboard`, `cloudwatch.EventRule`, `cloudwatch.LogGroup`, and `sqs.Queue`.
[Ruby on Rails](aws-ts-ruby-on-rails) | Create a single EC2 virtual machine instance with a local MySQL database.
[S3 Lambda](aws-ts-s3-lambda-copyzip) | Set up two AWS S3 Buckets and a single Lambda that listens to one and, upon each new object arriving in it, zips it up and copies it to the second bucket.
[Serverless Application](aws-ts-serverless-raw) | Deploy a complete serverless C# application using raw resources from `@pulumi/aws`.
[Serverless Datawarehouse](aws-ts-serverless-datawarehouse) | Deploy a serverless data warehouse.
[Slackbot](aws-ts-slackbot) | Create a simple slackbot that posts a notification to a specific channel any time you're @mentioned anywhere.
[Stack Reference](aws-ts-stackreference) | Create a "team" EC2 Instance with tags set from upstream stacks.
[Static Website](aws-ts-static-website) | Serve a static website using S3, CloudFront, Route53, and Certificate Manager.
[Step Functions](aws-ts-stepfunctions) | Use Step Functions with a Lambda function.
[Thumbnailer](aws-ts-thumbnailer) | Create a video thumbnail extractor using serverless functions and containers.
[Twitter](aws-ts-twitter-athena) | Query Twitter every 2 minutes, store the results in S3, and set up an Athena table and query.
[Voting App](aws-ts-voting-app) | Create a simple voting app using Redis and Python Flask.
[Web Server](aws-ts-webserver) | Deploy an EC2 Virtual machine using TypeScript to run a Python web server.
[Web Server with Manual Provisioning](aws-ts-ec2-provisioners) | Use Pulumi dynamic providers to accomplish post-provisioning configuration steps.
[LangServe - Hello OpenAI](aws-ts-langserve) | Deploy a LangServe app that uses OpenAI's on AWS ECS.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### Python

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[API Gateway HTTP API quickstart](aws-py-apigatewayv2-http-api-quickcreate) | Deploy a very simple HTTP API that invokes a Lambda.
[API Gateway V2 with EventBridge and Lambda](aws-py-apigatewayv2-eventbridge) | Deploy an HTTP API that uses EventBridge to target a Lambda function.
[AppSync](aws-py-appsync) | Deploy a basic GraphQL endpoint in AWS AppSync.
[AssumeRole](aws-py-assume-role) | Use AssumeRole to create resources.
[Fargate](aws-py-fargate) | Provision a full ECS Fargate cluster running a load-balanced nginx web server.
[Resources](aws-py-resources) | Create various resources, including `cloudwatch.Dashboard`, `cloudwatch.EventRule`, `cloudwatch.LogGroup`, and `sqs.Queue`.
[S3 Folder](aws-py-s3-folder) | Serve a static website on S3.
[Stack Reference](aws-py-stackreference) | Create a "team" EC2 Instance with tags set from upstream stacks.
[Step Functions](aws-py-stepfunctions) | Use Step Functions with a Lambda function.
[Web Server](aws-py-webserver) | Deploy an EC2 instance and open port 80.
[LangServe - Hello OpenAI](aws-py-langserve) | Deploy a LangServe app that uses OpenAI's on AWS ECS.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### Go

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[AssumeRole](aws-go-assume-role) | Use AssumeRole to create resources.
[Fargate](aws-go-fargate) | Provision a full ECS Fargate cluster running a load-balanced nginx web server.
[Lambda](aws-go-lambda) | Create a lambda that does a simple `ToUpper` on the string input and returns it.
[S3 Folder](aws-go-s3-folder) | Serve a static website on S3.
[Web Server](aws-go-webserver) | Deploy an EC2 Virtual machine running a Python web server.
[LangServe - Hello OpenAI](aws-go-langserve) | Deploy a LangServe app that uses OpenAI's on AWS ECS.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### C#

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[AssumeRole](aws-cs-assume-role) | Use AssumeRole to create resources.
[Fargate](aws-cs-fargate) | Build, deploy, and run a Dockerized app using ECS, ECR, and Fargate.
[Lambda](aws-cs-lambda) | Create a lambda that does a simple `ToUpper` on the string input and returns it.
[S3 Folder](aws-cs-s3-folder) | Serve a static website on S3.
[Web Server](aws-cs-webserver) | Deploy an EC2 instance and open port 80.
[LangServe - Hello OpenAI](aws-cs-langserve) | Deploy a LangServe app that uses OpenAI's on AWS ECS.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### F#

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Lambda Web Server](aws-fs-lambda-webserver) | Create a web server in AWS lambda using the Giraffe web server.
[S3 Folder](aws-fs-s3-folder) | Serve a static website on S3.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

## Azure

### TypeScript

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Azure Container Apps](azure-ts-containerapps) | Run a Docker image on Azure Container Apps.
[Azure Container Instance](azure-ts-aci) | Run Azure Container Instances on Linux.
[Azure Kubernetes Service](azure-ts-aks) | Create an Azure Kubernetes Service (AKS) Cluster.
[Azure App Service](azure-ts-appservice) | Build a web application hosted in App Service and provision Azure SQL Database and Azure Application Insights.
[Azure App Service with Docker](azure-ts-appservice-docker) | Build a web application hosted in App Service from Docker images.
[App Service in Virtual Network](azure-ts-webapp-privateendpoint-vnet-injection) | Deploy two App Services - Front web app with VNet injection and Back web app with a Private Endpoint.
[Azure Cosmos DB and LogicApp](azure-ts-cosmosdb-logicapp) | Define Cosmos DB, API connections, and link them to a logic app.
[Azure Functions](azure-ts-functions) | Deploy a Node.js serverless function to Azure Functions.
[Azure Functions - Many](azure-ts-functions-many) | Deploy several kinds of Azure Functions created from raw deployment packages.
[Azure SDK integration](azure-ts-call-azure-sdk) | Call Azure SDK functions from a Pulumi program.
[Static Website](azure-ts-static-website) | Configure static website hosting in Azure Storage.
[Azure Synapse](azure-ts-synapse) | Starting point for enterprise analytics solutions based on Azure Synapse.
[Web Server](azure-ts-webserver) | Provision a Linux web server in an Azure Virtual Machine.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### Python

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Azure Container Apps](azure-py-containerapps) | Run a Docker image on Azure Container Apps.
[Azure Container Instance](azure-py-aci) | Run Azure Container Instances on Linux.
[Azure Kubernetes Service](azure-py-aks) | Create an Azure Kubernetes Service (AKS) Cluster.
[Azure App Service](azure-py-appservice) | Build a web application hosted in App Service and provision Azure SQL Database and Azure Application Insights.
[Azure App Service with Docker](azure-py-appservice-docker) | Build a web application hosted in App Service from Docker images.
[Azure SDK integration](azure-py-call-azure-sdk) | Call Azure SDK functions from a Pulumi program in Python.
[Azure Cosmos DB and LogicApp](azure-py-cosmosdb-logicapp) | Define Cosmos DB, API connections, and link them to a logic app.
[Minecraft Server](azure-py-minecraft-server) | Deploy an Azure Virtual Machine and provision a Minecraft server.
[Static Website](azure-py-static-website) | Configure static website hosting in Azure Storage.
[Azure Synapse](azure-py-synapse) | Starting point for enterprise analytics solutions based on Azure Synapse.
[Virtual Data Center](azure-py-virtual-data-center) | Deploy Azure Virtual Data Center (VDC) hub-and-spoke network stacks in Azure, complete with ExpressRoute and VPN Gateways, Azure Firewall guarding a DMZ, and Azure Bastion.
[Web Server](azure-py-webserver) | Provision a Linux web server in an Azure Virtual Machine.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### Go

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Azure Container Apps](azure-go-containerapps) | Run a Docker image on Azure Container Apps.
[Azure Container Instance](azure-go-aci) | Run Azure Container Instances on Linux.
[Azure Kubernetes Service](azure-go-aks) | Create an Azure Kubernetes Service (AKS) Cluster.
[Azure App Service with Docker](azure-go-appservice-docker) | Build a web application hosted in App Service from Docker images.
[Static Website](azure-go-static-website) | Configure static website hosting in Azure Storage.
[Azure SDK integration](azure-go-call-azure-sdk) | Call Azure SDK functions from a Pulumi programin Go.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### C#

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
Cluster.
[Azure Container Apps](azure-cs-containerapps) | Run a Docker image on Azure Container Apps.
[Azure Container Instance](azure-cs-aci) | Run Azure Container Instances on Linux.
[Azure Kubernetes Service](azure-cs-aks) | Create an Azure Kubernetes Service (AKS) Cluster.
[AKS web app with .NET 5](azure-cs-net5-aks-webapp) | Create an Azure Kubernetes Service (AKS) cluster and deploy a web app to it using .NET 5 and C# 9.
[AKS + Cosmos DB](azure-cs-aks-cosmos-helm) | A Helm chart deployed to AKS that stores TODOs in an Azure Cosmos DB MongoDB API.
[Azure App Service](azure-cs-appservice) | Build a web application hosted in App Service and provision Azure SQL Database and Azure Application Insights.
[Azure App Service with Docker](azure-cs-appservice-docker) | Build a web application hosted in App Service from Docker images.
[Azure API integration](azure-cs-call-azure-api) | Call additional Azure API endpoints from a Pulumi program.
[Azure Cosmos DB and LogicApp](azure-cs-cosmosdb-logicapp) | Define Cosmos DB, API connections, and link them to a logic app.
[Azure Functions](azure-cs-functions) | Deploy a Node.js serverless function to Azure Functions.
[Static Website](azure-cs-static-website) | Configure static website hosting in Azure Storage.
[Azure Synapse](azure-cs-synapse) | Starting point for enterprise analytics solutions based on Azure Synapse.
[Azure SQL Server](azure-cs-sqlserver) | An example of a SQLServer on Azure PaaS.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

## GCP

### TypeScript

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Cloud Run](gcp-ts-cloudrun) | Deploy a custom Docker image into Google Cloud Run service.
[Functions - Raw](gcp-ts-serverless-raw) | Deploy two Google Cloud Functions implemented in Python and Go.
[Functions](gcp-ts-functions) | Deploy an HTTP Google Cloud Function endpoint.
[GKE - Hello World](gcp-ts-gke-hello-world) | Deploy a GKE cluster, then a Kubernetes namespace and nginx deployment into the cluster.
[GKE](gcp-ts-gke) | Provision a Google Kubernetes Engine (GKE) cluster, then a Kubernetes Deployment.
[Ruby on Rails](gcp-ts-k8s-ruby-on-rails-postgresql) | Deliver a containerized Ruby on Rails application.
[Slackbot](gcp-ts-slackbot) | Create a simple slackbot that posts a notification to a specific channel any time you're @mentioned anywhere.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### Python

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Functions - Raw](gcp-py-serverless-raw) | Deploy two Google Cloud Functions implemented in Python and Go.
[Functions](gcp-py-functions) | Deploy a Python-based Google Cloud Function.
[GKE](gcp-py-gke) | Provision a Google Kubernetes Engine (GKE) cluster, then a Kubernetes Deployment.
[Network Component](gcp-py-network-component) | Use a reusable component to create a Google Cloud Network and instance.
[nginx Server](gcp-py-instance-nginx) | Build a nginx server in Google Cloud.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### Go

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Functions](gcp-go-functions) | Deploy a Go-based Google Cloud Function.
[Functions - Raw](gcp-py-serverless-raw) | Deploy a Google Cloud Function implemented in Python.
[Web Server](gcp-go-webserver) | Build a web server in Google Cloud.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### C#

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Functions - Raw](gcp-py-serverless-raw) | Deploy a Google Cloud Function implemented in Python.
[Functions](gcp-go-functions) | Deploy a Go-based Google Cloud Function.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

## Kubernetes

### TypeScript

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[App Rollout via ConfigMap](kubernetes-ts-configmap-rollout) | Enable a change in a ConfigMap to trigger a rollout of an nginx Deployment.
[App Rollout via S3 Data Change](kubernetes-ts-s3-rollout) | Enable a change in data in S3 to trigger a rollout of an nginx deployment.
[Expose Deployment](kubernetes-ts-exposed-deployment) | Deploy nginx to a Kubernetes cluster, and publicly explose it using a Kubernetes Service.
[Guestbook](kubernetes-ts-guestbook) | Build and deploy a simple, multi-tier web application using Kubernetes and Docker.
[Jenkins](kubernetes-ts-jenkins) | Deploy a container running the Jenkins continuous integration system onto a running Kubernetes cluster.
[Multicloud](kubernetes-ts-multicloud) | Create managed Kubernetes clusters using AKS, EKS, and GKE, and deploy the application on each cluster.
[nginx server](kubernetes-ts-nginx) | Deploy a replicated nginx server to a Kubernetes cluster, using TypeScript and no YAML.
[Sock Shop](kubernetes-ts-sock-shop) | Deploy a version of the standard Sock Shop microservices reference app.
[Staged App Rollout](kubernetes-ts-staged-rollout-with-prometheus) | Create a staged rollout gated by checking that the P90 response time reported by Prometheus is less than some amount.
[Wordpress Helm Chart](kubernetes-ts-helm-wordpress) | Use the Helm API to deploy v2.1.3 of the Wordpress Helm Chart to a Kubernetes cluster.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### Python

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Guestbook](kubernetes-py-guestbook) | Build and deploy a simple, multi-tier web application using Kubernetes and Docker.
[Self-Host Gemma 4](kubernetes-py-self-host-gemma4-llm) | Deploy Open WebUI on Kubernetes with host-native Gemma 4 inference and Tailscale access.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### C#

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Guestbook](kubernetes-cs-guestbook) | Build and deploy a simple, multi-tier web application using Kubernetes and Docker.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### Go

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Guestbook](kubernetes-go-guestbook) | Build and deploy a simple, multi-tier web application using Kubernetes and Docker.
[App Rollout via ConfigMap](kubernetes-go-configmap-rollout) | Enable a change in a ConfigMap to trigger a rollout of an nginx Deployment.
[Wordpress Helm Chart](kubernetes-go-helm-wordpress) | Use the Helm API to deploy v9.6.0 of the Wordpress Helm Chart to a Kubernetes cluster.
[Expose Deployment](kubernetes-go-exposed-deployment) | Deploy nginx to a Kubernetes cluster, and publicly expose it using a Kubernetes Service.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

## Openstack

### Python

[🔝 Back to the list](#all-pulumi-examples)

[Web Server](openstack-py-webserver) | Deploy an Openstack instance and open port 8000.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

## OVHCloud

### Go

| Example                              | Description |
|--------------------------------------| --------- |
| [Kubernetes](ovhcloud-go-kubernetes) | A sample to deploy a managed Kubernetes cluster on OVHcloud |

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

## DigitalOcean

### TypeScript

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Droplets](digitalocean-ts-loadbalanced-droplets) | Build sample architecture.
[Kubernetes](digitalocean-ts-k8s) | Provision a DigitalOcean Kubernetes cluster.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### Python

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Droplets](digitalocean-py-loadbalanced-droplets) | Build sample architecture.
[Kubernetes](digitalocean-py-k8s) | Provision a DigitalOcean Kubernetes cluster.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

### C#

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Droplets](digitalocean-cs-loadbalanced-droplets) | Build sample architecture.
[Kubernetes](digitalocean-cs-k8s) | Provision a DigitalOcean Kubernetes cluster.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

## Multicloud

### TypeScript

[🔝 Back to the list](#all-pulumi-examples)

[Try Pulumi Copilot](https://app.pulumi.com/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) and use natural-language prompts to generate Pulumi example programs in _any_ language.

Example   | Description |
--------- | --------- |
[Buckets](multicloud-ts-buckets) | Use a single Pulumi program to provision resources in both AWS and GCP.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

## F5

### TypeScript

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[BigIP Local Traffic Manager](f5bigip-ts-ltm-pool) | Provide load balancing via an F5 BigIP appliance to backend HTTP instances.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

## Twilio

### TypeScript

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Component](twilio-ts-component) | Create a custom Component Resource to parse incoming messages from Twilio.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

## Linode

### JavaScript

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
--------- | --------- |
[Web Server](linode-js-webserver) | Build a web server on Linode.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

## Testing

[🔝 Back to the list](#all-pulumi-examples)

Example   | Description |
-----          | --------- |
[Unit Tests in TypeScript](testing-unit-ts)      | Mock-based unit tests in TypeScript.
[Unit Tests in Python](testing-unit-py)          | Mock-based unit tests in Python.
[Unit Tests in Go](testing-unit-go)              | Mock-based unit tests in Go.
[Unit Tests in C#](testing-unit-cs)              | Mock-based unit tests in C#.
[Testing with Policies](testing-pac-ts)          | Tests based on Policy-as-Code in TypeScript.
[Integration Testing in Go](testing-integration) | Deploy-check-destroy tests in Go.

[Use Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=pulumi-examples) to build a new example in _any_ language.

## Automation API

[🔝 Back to the list](#all-pulumi-examples)

[Automation API Examples](https://github.com/pulumi/automation-api-examples)

## Community

Engage with our community to elevate your developer experience:

- **Join our online [Pulumi Community on Slack](https://slack.pulumi.com/?utm_campaign=pulumi-pulumi-examples-repo&utm_source=github.com&utm_medium=welcome-slack)** - Interact with thousands of Pulumi developers for collaborative problem-solving and knowledge-sharing!
- **Join a [Local Pulumi User Groups (PUGs)](https://www.meetup.com/pro/pugs/)**-  Attend tech-packed meetups and hands-on virtual or in-person workshops.
- **Follow [@PulumiCorp](https://twitter.com/PulumiCorp) on X (Twitter)** - Get real-time updates, technical insights, and sneak peeks into the latest features.
- **Subscribe to our YouTube Channel, [PulumiTV](https://www.youtube.com/@PulumiTV)** - Learn about AI / ML essentials, launches, workshops, demos and more.
- **Follow our [LinkedIn](https://www.linkedin.com/company/pulumi/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=examples-community)** - Uncover company news, achievements, and behind-the-scenes glimpses.

## Contributors

Meet the [brilliant minds behind this project](https://github.com/pulumi/examples/graphs/contributors), view their profiles, and learn about their valuable contributions.

Want to contribute an example? Please visit our [CONTRIBUTING](CONTRIBUTING.md) doc for details.

## Pulumi developer resources

Delve deeper into our project with additional resources:

- [Get Started with Pulumi](https://www.pulumi.com/docs/get-started/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=examples-resources): Deploy a simple application in AWS, Azure, Google Cloud, or Kubernetes using Pulumi.
- [Documentation](https://www.pulumi.com/docs/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=examples-resources): Learn about Pulumi concepts, follow user guides, and consult the reference documentation.
- [Pulumi Blog](https://www.pulumi.com/blog/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=examples-resources) - Stay in the loop with our latest tech announcements, insightful articles, and updates.
- [Registry](https://www.pulumi.com/registry/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=examples-resources): Search for packages and learn about the supported resources you need. Install the package directly into your project, browse the API documentation, and start building.
- [Try Pulumi AI](https://www.pulumi.com/ai/?utm_campaign=pulumi-examples-github-repo&utm_source=github.com&utm_medium=examples-resources) - Use natural-language prompts to generate Pulumi infrastructure-as-code programs in any language.

## Pulumi roadmap

Review the planned work for the upcoming quarter and a selected backlog of issues that are on our mind but not yet scheduled on the [Pulumi Roadmap.](https://github.com/orgs/pulumi/projects/44)

=== aws-py-s3-folder ===
[![Deploy this example with Pulumi](https://www.pulumi.com/images/deploy-with-pulumi/dark.svg)](https://app.pulumi.com/new?template=https://github.com/pulumi/examples/blob/master/aws-py-s3-folder/README.md#gh-light-mode-only)
[![Deploy this example with Pulumi](https://get.pulumi.com/new/button-light.svg)](https://app.pulumi.com/new?template=https://github.com/pulumi/examples/blob/master/aws-py-s3-folder/README.md#gh-dark-mode-only)

# Host a Static Website on Amazon S3

A static website that uses [S3's website support](https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html).
For a detailed walkthrough of this example, see the tutorial [Static Website on AWS S3](https://www.pulumi.com/docs/tutorials/aws/s3-website/).

## Deploying and running the program

Note: some values in this example will be different from run to run.  These values are indicated
with `***`.

1. Create a new stack:

    ```bash
    $ pulumi stack init website-testing
    ```

1. Set the AWS region:

    ```bash
    $ pulumi config set aws:region us-west-2
    ```

1. Run `pulumi up` to preview and deploy changes.  After the preview is shown you will be
    prompted if you want to continue or not.

    ```bash
    $ pulumi up
    Previewing update (dev):

        Type                    Name                  Plan
    +   pulumi:pulumi:Stack     aws-py-s3-folder-dev  create
    +   ├─ aws:s3:Bucket        s3-website-bucket     create
    +   ├─ aws:s3:BucketObject  index.html            create
    +   ├─ aws:s3:BucketObject  python.png            create
    +   ├─ aws:s3:BucketObject  favicon.png           create
    +   └─ aws:s3:BucketPolicy  bucket-policy         create

    Resources:
        + 6 to create

    Do you want to perform this update?
    > yes
      no
      details
    ```

1. To see the resources that were created, run `pulumi stack output`:

    ```bash
    $ pulumi stack output
    Current stack outputs (2):
        OUTPUT                                           VALUE
        bucket_name                                      s3-website-bucket-***
        website_url                                      ***.s3-website-us-west-2.amazonaws.com
    ```

1. To see that the S3 objects exist, you can either use the AWS Console or the AWS CLI:

    ```bash
    $ aws s3 ls $(pulumi stack output bucket_name)
    2018-04-17 15:40:47      13731 favicon.png
    2018-04-17 15:40:48        249 index.html
    ```

1. Open the site URL in a browser to see both the rendered HTML, the favicon, and Python splash image:

    ```bash
    $ pulumi stack output website_url
    ***.s3-website-us-west-2.amazonaws.com
    ```

1. To clean up resources, run `pulumi destroy` and answer the confirmation question at the prompt.

```python
import json
import mimetypes
import os

from pulumi import FileAsset, Output, export, ResourceOptions
from pulumi_aws import s3

web_bucket = s3.Bucket("s3-website-bucket")

web_site = s3.BucketWebsiteConfiguration(
    "s3-website", bucket=web_bucket.bucket, index_document={"suffix": "index.html"}
)

public_access_block = s3.BucketPublicAccessBlock(
    "public-access-block", bucket=web_bucket.id, block_public_acls=False
)

content_dir = "www"
for file in os.listdir(content_dir):
    filepath = os.path.join(content_dir, file)
    mime_type, _ = mimetypes.guess_type(filepath)
    obj = s3.BucketObject(
        file, bucket=web_bucket.id, source=FileAsset(filepath), content_type=mime_type
    )


def public_read_policy_for_bucket(bucket_name):
    return Output.json_dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [
                        Output.format("arn:aws:s3:::{0}/*", bucket_name),
                    ],
                }
            ],
        }
    )


bucket_name = web_bucket.id
bucket_policy = s3.BucketPolicy(
    "bucket-policy",
    bucket=bucket_name,
    policy=public_read_policy_for_bucket(bucket_name),
    opts=ResourceOptions(depends_on=[public_access_block]),
)

# Export the name of the bucket
export("bucket_name", web_bucket.id)
export("website_url", web_site.website_endpoint)
```

=== aws-py-fargate ===
[![Deploy this example with Pulumi](https://www.pulumi.com/images/deploy-with-pulumi/dark.svg)](https://app.pulumi.com/new?template=https://github.com/pulumi/examples/blob/master/aws-py-fargate/README.md#gh-light-mode-only)
[![Deploy this example with Pulumi](https://get.pulumi.com/new/button-light.svg)](https://app.pulumi.com/new?template=https://github.com/pulumi/examples/blob/master/aws-py-fargate/README.md#gh-dark-mode-only)

# NGINX on AWS ECS Fargate using Python

This example shows authoring Infrastructure as Code in Python. It
provisions a full [Amazon Elastic Container Service (ECS) "Fargate"](https://aws.amazon.com/ecs) cluster and
related infrastructure, running a load-balanced NGINX web server accessible over the Internet on port 80.
This example is inspired by [Docker's Getting Started Tutorial](https://docs.docker.com/get-started/).

## Prerequisites

* [Install Pulumi](https://www.pulumi.com/docs/get-started/install/)
* [Configure Pulumi to Use AWS](https://www.pulumi.com/docs/intro/cloud-providers/aws/setup/) (if your AWS CLI is configured, no further changes are required)

## Running the Example

Clone [the examples repo](https://github.com/pulumi/examples/tree/master/aws-py-fargate) and `cd` into it.

Next, to deploy the application and its infrastructure, follow these steps:

1. Create a new stack, which is an isolated deployment target for this example:

    ```bash
    $ pulumi stack init dev
    ```

1. Set your desired AWS region:

    ```bash
    $ pulumi config set aws:region us-east-1 # any valid AWS region will work
    ```

1. Deploy everything with a single `pulumi up` command. This will show you a preview of changes first, which
   includes all of the required AWS resources (clusters, services, and the like). Don't worry if it's more than
   you expected -- this is one of the benefits of Pulumi, it configures everything so that so you don't need to!

    ```bash
    $ pulumi up
    ```

    After being prompted and selecting "yes", your deployment will begin. It'll complete in a few minutes:

    ```bash
    Updating (dev):
         Type                             Name                Status
     +   pulumi:pulumi:Stack              aws-py-fargate-dev  created
     +   ├─ aws:ecs:Cluster               cluster             created
     +   ├─ aws:ec2:SecurityGroup         web-secgrp          created
     +   ├─ aws:iam:Role                  task-exec-role      created
     +   ├─ aws:lb:TargetGroup            app-tg              created
     +   ├─ aws:ecs:TaskDefinition        app-task            created
     +   ├─ aws:iam:RolePolicyAttachment  task-exec-policy    created
     +   ├─ aws:lb:LoadBalancer           app-lb              created
     +   ├─ aws:lb:Listener               web                 created
     +   └─ aws:ecs:Service               app-svc             created

    Outputs:
        url: "app-lb-ad43707-1433933240.us-west-2.elb.amazonaws.com"

    Resources:
        + 10 created

    Duration: 2m56s

    Permalink: https://app.pulumi.com/acmecorp/aws-python-fargate/dev/updates/1
    ```

   Notice that the automatically assigned load-balancer URL is printed as a stack output.

1. At this point, your app is running -- let's curl it. The CLI makes it easy to grab the URL:

    ```bash
    $ curl http://$(pulumi stack output url)
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>
    <style>
        body {
            width: 35em;
            margin: 0 auto;
            font-family: Tahoma, Verdana, Arial, sans-serif;
        }
    </style>
    </head>
    <body>
    <h1>Welcome to nginx!</h1>
    <p>If you see this page, the nginx web server is successfully installed and
    working. Further configuration is required.</p>

    <p>For online documentation and support please refer to
    <a href="http://nginx.org/">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="http://nginx.com/">nginx.com</a>.</p>

    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>
    ```

**Please Note**: It may take a few minutes for the app to start up. Until that point, you may receive a 503 error response code.

1. Try making some changes, and rerunning `pulumi up`. For example, let's scale up to 3 instances:

    Running `pulumi up` will show you the delta and then, after confirming, will deploy just those changes:

    ```bash
    $ pulumi up
    ```

    Notice that `pulumi up` redeploys just the parts of the application/infrastructure that you've edited.

    ```bash
        Updating (dev):

         Type                 Name                Status      Info
         pulumi:pulumi:Stack  aws-py-fargate-dev
     ~   └─ aws:ecs:Service   app-svc             updated     [diff: ~desiredCount]

    Outputs:
        url: "app-lb-ad43707-1433933240.us-west-2.elb.amazonaws.com"

    Resources:
        ~ 1 updated
        9 unchanged

    Duration: 14s

    Permalink: https://app.pulumi.com/acmecorp/aws-python-fargate/dev/updates/2
    ```

1. Once you are done, you can destroy all of the resources, and the stack:

    ```bash
    $ pulumi destroy
    $ pulumi stack rm
    ```

```python
from pulumi import export, ResourceOptions
import pulumi_aws as aws
import json

# Create an ECS cluster to run a container-based service.
cluster = aws.ecs.Cluster("cluster")

# Read back the default VPC and public subnets, which we will use.
default_vpc = aws.ec2.get_vpc(default=True)
default_vpc_subnets = aws.ec2.get_subnets(
    filters=[
        {
            "name": "vpc-id",
            "values": [default_vpc.id],
        }
    ],
)

# Create a SecurityGroup that permits HTTP ingress and unrestricted egress.
group = aws.ec2.SecurityGroup(
    "web-secgrp",
    vpc_id=default_vpc.id,
    description="Enable HTTP access",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"],
        }
    ],
    egress=[
        {
            "protocol": "-1",
            "from_port": 0,
            "to_port": 0,
            "cidr_blocks": ["0.0.0.0/0"],
        }
    ],
)

# Create a load balancer to listen for HTTP traffic on port 80.
alb = aws.lb.LoadBalancer(
    "app-lb",
    security_groups=[group.id],
    subnets=default_vpc_subnets.ids,
)

atg = aws.lb.TargetGroup(
    "app-tg",
    port=80,
    protocol="HTTP",
    target_type="ip",
    vpc_id=default_vpc.id,
)

wl = aws.lb.Listener(
    "web",
    load_balancer_arn=alb.arn,
    port=80,
    default_actions=[
        {
            "type": "forward",
            "target_group_arn": atg.arn,
        }
    ],
)

# Create an IAM role that can be used by our service's task.
role = aws.iam.Role(
    "task-exec-role",
    assume_role_policy=json.dumps(
        {
            "Version": "2008-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }
    ),
)

rpa = aws.iam.RolePolicyAttachment(
    "task-exec-policy",
    role=role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
)

# Spin up a load balanced service running our container image.
task_definition = aws.ecs.TaskDefinition(
    "app-task",
    family="fargate-task-definition",
    cpu="256",
    memory="512",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=role.arn,
    container_definitions=json.dumps(
        [
            {
                "name": "my-app",
                "image": "nginx",
                "portMappings": [{"containerPort": 80, "hostPort": 80, "protocol": "tcp"}],
            }
        ]
    ),
)

service = aws.ecs.Service(
    "app-svc",
    cluster=cluster.arn,
    desired_count=3,
    launch_type="FARGATE",
    task_definition=task_definition.arn,
    network_configuration={
        "assign_public_ip": True,
        "subnets": default_vpc_subnets.ids,
        "security_groups": [group.id],
    },
    load_balancers=[
        {
            "target_group_arn": atg.arn,
            "container_name": "my-app",
            "container_port": 80,
        }
    ],
    opts=ResourceOptions(depends_on=[wl]),
)

export("url", alb.dns_name)
```

=== aws-py-eks ===
[![Deploy this example with Pulumi](https://www.pulumi.com/images/deploy-with-pulumi/dark.svg)](https://app.pulumi.com/new?template=https://github.com/pulumi/examples/blob/master/aws-py-eks/README.md#gh-light-mode-only)
[![Deploy this example with Pulumi](https://get.pulumi.com/new/button-light.svg)](https://app.pulumi.com/new?template=https://github.com/pulumi/examples/blob/master/aws-py-eks/README.md#gh-dark-mode-only)

# Amazon EKS Cluster

This example deploys an EKS Kubernetes cluster inside a AWS VPC with proper NodeGroup and Networking Configured

## Deploying the App

To deploy your infrastructure, follow the below steps.

## Prerequisites

1. [Install Pulumi](https://www.pulumi.com/docs/get-started/install/)
1. [Configure Pulumi for AWS](https://www.pulumi.com/docs/intro/cloud-providers/aws/setup/)
1. [Configure Pulumi for Python](https://www.pulumi.com/docs/intro/languages/python/)
1. *Optional for K8 Auth* [Install `iam-authenticator`](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html)

## Deploying and running the program

1.  Create a new stack:

    ```
    $ pulumi stack init python-eks-testing
    ```

1.  Set the AWS region:

    ```
    $ pulumi config set aws:region us-east-2
    ```

1.  Run `pulumi up` to preview and deploy changes:

    ```
    $ pulumi up
        Previewing stack 'python-eks-testing'
        Previewing changes:
        ...

        Do you want to perform this update? yes
        Updating (python-eks-testing):

            Type                              Name                                Status
        +   pulumi:pulumi:Stack               aws-py-eks-python-eks-testing       created
        +   ├─ aws:iam:Role                   ec2-nodegroup-iam-role              created
        +   ├─ aws:iam:Role                   eks-iam-role                        created
        +   ├─ aws:ec2:Vpc                    eks-vpc                             created
        +   ├─ aws:iam:RolePolicyAttachment   eks-workernode-policy-attachment    created
        +   ├─ aws:iam:RolePolicyAttachment   eks-cni-policy-attachment           created
        +   ├─ aws:iam:RolePolicyAttachment   ec2-container-ro-policy-attachment  created
        +   ├─ aws:iam:RolePolicyAttachment   eks-service-policy-attachment       created
        +   ├─ aws:iam:RolePolicyAttachment   eks-cluster-policy-attachment       created
        +   ├─ aws:ec2:InternetGateway        vpc-ig                              created
        +   ├─ aws:ec2:Subnet                 vpc-sn-1                            created
        +   ├─ aws:ec2:Subnet                 vpc-sn-2                            created
        +   ├─ aws:ec2:SecurityGroup          eks-cluster-sg                      created
        +   ├─ aws:ec2:RouteTable             vpc-route-table                     created
        +   ├─ aws:eks:Cluster                eks-cluster                         created
        +   ├─ aws:ec2:RouteTableAssociation  vpc-1-route-table-assoc             created
        +   ├─ aws:ec2:RouteTableAssociation  vpc-2-route-table-assoc             created
        +   └─ aws:eks:NodeGroup              eks-node-group                      created

        Outputs:
            cluster-name: "eks-cluster-96b87e8"

        Resources:
            + 18 created

        Duration: 14m15s

    ```

1.  View the cluster name via `stack output`:

    ```
    $ pulumi stack output
        Current stack outputs (1):
        OUTPUT                   VALUE
        cluster-name  eks-cluster-96b87e8
    ```

1.  Verify that the EKS cluster exists, by either using the AWS Console or running `aws eks list-clusters`.

1. Update your KubeConfig, Authenticate to your Kubernetes Cluster and verify you have API access and nodes running.

```
$ aws eks --region us-east-2 update-kubeconfig --name $(pulumi stack output cluster-name)

    Added new context arn:aws:eks:us-east-2:account:cluster/eks-cluster-96b87e8
```


```
$ kubectl get nodes

    NAME                                         STATUS   ROLES    AGE   VERSION
    ip-10-100-0-182.us-east-2.compute.internal   Ready    <none>   10m   v1.14.7-eks-1861c5
    ip-10-100-1-174.us-east-2.compute.internal   Ready    <none>   10m   v1.14.7-eks-1861c5
```

## Clean up

To clean up resources, run `pulumi destroy` and answer the confirmation question at the prompt.

```python
import iam
import vpc
import utils
import pulumi
from pulumi_aws import eks

## EKS Cluster

eks_cluster = eks.Cluster(
    "eks-cluster",
    role_arn=iam.eks_role.arn,
    tags={
        "Name": "pulumi-eks-cluster",
    },
    vpc_config=eks.ClusterVpcConfigArgs(
        public_access_cidrs=["0.0.0.0/0"],
        security_group_ids=[vpc.eks_security_group.id],
        subnet_ids=vpc.subnet_ids,
    ),
)

eks_node_group = eks.NodeGroup(
    "eks-node-group",
    cluster_name=eks_cluster.name,
    node_group_name="pulumi-eks-nodegroup",
    node_role_arn=iam.ec2_role.arn,
    subnet_ids=vpc.subnet_ids,
    tags={
        "Name": "pulumi-cluster-nodeGroup",
    },
    scaling_config=eks.NodeGroupScalingConfigArgs(
        desired_size=2,
        max_size=2,
        min_size=1,
    ),
)

pulumi.export("cluster-name", eks_cluster.name)
pulumi.export("kubeconfig", utils.generate_kube_config(eks_cluster))
```

=== aws-py-serverless-raw ===
[![Deploy this example with Pulumi](https://www.pulumi.com/images/deploy-with-pulumi/dark.svg)](https://app.pulumi.com/new?template=https://github.com/pulumi/examples/blob/master/aws-py-serverless-raw/README.md#gh-light-mode-only)
[![Deploy this example with Pulumi](https://get.pulumi.com/new/button-light.svg)](https://app.pulumi.com/new?template=https://github.com/pulumi/examples/blob/master/aws-py-serverless-raw/README.md#gh-dark-mode-only)

# Serverless C# App

This example deploys a complete serverless C# application using raw `aws.apigateway.RestApi`, `aws.lambda_.Function` and
`aws.dynamodb.Table` resources from `pulumi_aws`.  Although this doesn't feature any of the higher-level abstractions
from the `pulumi_cloud` package, it demonstrates that you can program the raw resources directly available in AWS
to accomplish all of the same things this higher-level package offers.

The deployed Lambda function is a simple C# application, highlighting the ability to manage existing application code
in a Pulumi application, even if your Pulumi code is written in a different language like JavaScript or Python.

The Lambda function is a C# application using .NET Core 3.1 (a similar approach works for any other language supported by
AWS Lambda).

## Deploying and running the Pulumi App

1.  Create a new stack:

    ```bash
    $ pulumi stack init dev
    ```

1.  Build the C# application.

    ```bash
    dotnet publish app
    ```

1.  Set the AWS region:

    ```bash
    $ pulumi config set aws:region us-east-2
    ```

1.  Optionally, set AWS Lambda provisioned concurrency:

    ```bash
    $ pulumi config set provisionedConcurrency 1
    ```

1.  Run `pulumi up` to preview and deploy changes:

    ```
    $ pulumi up
    Previewing update (dev):
    ...

    Updating (dev):
    ...
    Resources:
        + 10 created
    Duration: 1m 20s
    ```

1.  Check the deployed GraphQL endpoint:

    ```
    $ curl $(pulumi stack output endpoint)/hello
    {"Path":"/hello","Count":0}
    ```

1.  See the logs

    ```
    $ pulumi logs -f
    2018-03-21T18:24:52.670-07:00[    mylambda-d719650] START RequestId: d1e95652-2d6f-11e8-93f6-2921c8ae65e7 Version: $LATEST
    2018-03-21T18:24:56.171-07:00[    mylambda-d719650] Getting count for '/hello'
    2018-03-21T18:25:01.327-07:00[    mylambda-d719650] Got count 0 for '/hello'
    2018-03-21T18:25:02.267-07:00[    mylambda-d719650] END RequestId: d1e95652-2d6f-11e8-93f6-2921c8ae65e7
    2018-03-21T18:25:02.267-07:00[    mylambda-d719650] REPORT RequestId: d1e95652-2d6f-11e8-93f6-2921c8ae65e7   Duration: 9540.93 ms    Billed Duration: 9600 ms        Memory Size: 128 MB     Max Memory Used: 37 MB
    ```

## Clean up

1.  Run `pulumi destroy` to tear down all resources.

1.  To delete the stack itself, run `pulumi stack rm`. Note that this command deletes all deployment history from the Pulumi console.

```python
"""Copyright 2016-2019, Pulumi Corporation.  All rights reserved."""

import json

import pulumi
import pulumi_aws as aws

# The location of the built dotnet8.0 application to deploy
dotnet_application_publish_folder = "./app/bin/Release/net8.0/publish"
dotnet_application_entry_point = "app::app.Functions::GetAsync"
# The stage name to use for the API Gateway URL
custom_stage_name = "api"

region = aws.config.region

#################
## DynamoDB Table
#################

# A DynamoDB table with a single primary key
counter_table = aws.dynamodb.Table(
    "counterTable",
    attributes=[
        aws.dynamodb.TableAttributeArgs(
            name="Id",
            type="S",
        ),
    ],
    hash_key="Id",
    read_capacity=1,
    write_capacity=1,
)

##################
## Lambda Function
##################

# Give our Lambda access to the Dynamo DB table, CloudWatch Logs and Metrics
# Python package does not have assumeRolePolicyForPrinciple
instance_assume_role_policy = aws.iam.get_policy_document(
    statements=[
        aws.iam.GetPolicyDocumentStatementArgs(
            actions=["sts:AssumeRole"],
            principals=[
                aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    identifiers=["lambda.amazonaws.com"],
                    type="Service",
                )
            ],
        )
    ]
)

role = aws.iam.Role(
    "mylambda-role",
    assume_role_policy=instance_assume_role_policy.json,
)

policy = aws.iam.RolePolicy(
    "mylambda-policy",
    role=role.id,
    policy=pulumi.Output.json_dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "dynamodb:UpdateItem",
                        "dynamodb:PutItem",
                        "dynamodb:GetItem",
                        "dynamodb:DescribeTable",
                    ],
                    "Resource": counter_table.arn,
                    "Effect": "Allow",
                },
                {
                    "Action": ["logs:*", "cloudwatch:*"],
                    "Resource": "*",
                    "Effect": "Allow",
                },
            ],
        }
    ),
)

# Read the config of whether to provision fixed concurrency for Lambda
config = pulumi.Config()
provisioned_concurrent_executions = config.get_float("provisionedConcurrency")

# Create a Lambda function, using code from the `./app` folder.

lambda_func = aws.lambda_.Function(
    "mylambda",
    opts=pulumi.ResourceOptions(depends_on=[policy]),
    runtime="dotnet8",
    code=pulumi.AssetArchive(
        {
            ".": pulumi.FileArchive(dotnet_application_publish_folder),
        }
    ),
    timeout=300,
    handler=dotnet_application_entry_point,
    role=role.arn,
    publish=bool(provisioned_concurrent_executions),
    # Versioning required for provisioned concurrency
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={
            "COUNTER_TABLE": counter_table.name,
        },
    ),
)

if provisioned_concurrent_executions:
    concurrency = aws.lambda_.ProvisionedConcurrencyConfig(
        "concurrency",
        function_name=lambda_func.name,
        qualifier=lambda_func.version,
        provisioned_concurrent_executions=provisioned_concurrent_executions,
    )


#####################
## APIGateway RestAPI
######################


# Create a single Swagger spec route handler for a Lambda function.
def swagger_route_handler(arn):
    return {
        "x-amazon-apigateway-any-method": {
            "x-amazon-apigateway-integration": {
                "uri": pulumi.Output.format(
                    "arn:aws:apigateway:{0}:lambda:path/2015-03-31/functions/{1}/invocations",
                    region,
                    arn,
                ),
                "passthroughBehavior": "when_no_match",
                "httpMethod": "POST",
                "type": "aws_proxy",
            },
        },
    }


# Create the API Gateway Rest API, using a swagger spec.
rest_api = aws.apigateway.RestApi(
    "api",
    body=pulumi.Output.json_dumps(
        {
            "swagger": "2.0",
            "info": {"title": "api", "version": "1.0"},
            "paths": {
                "/{proxy+}": lambda_func.arn.apply(swagger_route_handler),
            },
        }
    ),
)

# Create a deployment of the Rest API.
deployment = aws.apigateway.Deployment(
    "api-deployment",
    rest_api=rest_api.id,
)

# Create a stage, which is an addressable instance of the Rest API. Set it to point at the latest deployment.
stage = aws.apigateway.Stage(
    "api-stage",
    rest_api=rest_api.id,
    deployment=deployment.id,
    stage_name=custom_stage_name,
)

# Give permissions from API Gateway to invoke the Lambda
invoke_permission = aws.lambda_.Permission(
    "api-lambda-permission",
    action="lambda:invokeFunction",
    function=lambda_func.name,
    principal="apigateway.amazonaws.com",
    source_arn=stage.execution_arn.apply(lambda arn: arn + "*/*"),
)

# Export the https endpoint of the running Rest API
pulumi.export("endpoint", stage.invoke_url.apply(lambda url: url + custom_stage_name))
```

=== aws-py-resources ===
[![Deploy this example with Pulumi](https://www.pulumi.com/images/deploy-with-pulumi/dark.svg)](https://app.pulumi.com/new?template=https://github.com/pulumi/examples/blob/master/aws-py-resources/README.md#gh-light-mode-only)
[![Deploy this example with Pulumi](https://get.pulumi.com/new/button-light.svg)](https://app.pulumi.com/new?template=https://github.com/pulumi/examples/blob/master/aws-py-resources/README.md#gh-dark-mode-only)

# AWS Resources

A Pulumi program that demonstrates creating various AWS resources in Python

```bash
# Create and configure a new stack
$ pulumi stack init dev
$ pulumi config set aws:region us-east-2

# Preview and run the deployment
$ pulumi up

# Remove the app
$ pulumi destroy
$ pulumi stack rm
```

```python
import json
from pulumi_aws import cloudwatch, sns, dynamodb, ec2, ecr, ecs, iam, kinesis, sqs

## CloudWatch
logins_topic = sns.Topic("myloginstopic")

event_rule = cloudwatch.EventRule(
    "myeventrule",
    event_pattern=json.dumps({"detail-type": ["AWS Console Sign In via CloudTrail"]}),
)

event_target = cloudwatch.EventTarget(
    "myeventtarget", rule=event_rule.name, target_id="SendToSNS", arn=logins_topic.arn
)

log_group = cloudwatch.LogGroup("myloggroup")

log_metric_filter = cloudwatch.LogMetricFilter(
    "mylogmetricfilter",
    pattern="",
    log_group_name=log_group.name,
    metric_transformation=cloudwatch.LogMetricFilterMetricTransformationArgs(
        name="EventCount",
        namespace="YourNamespace",
        value="1",
    ),
)

log_stream = cloudwatch.LogStream("mylogstream", log_group_name=log_group.name)

metric_alart = cloudwatch.MetricAlarm(
    "mymetricalarm",
    comparison_operator="GreaterThanOrEqualToThreshold",
    evaluation_periods=2,
    metric_name="CPUUtilization",
    namespace="AWS/EC2",
    period=120,
    statistic="Average",
    threshold=80,
    alarm_description="This metric monitors ec2 cpu utilization",
)

## DynamoDB
db = dynamodb.Table(
    "mytable",
    attributes=[
        dynamodb.TableAttributeArgs(
            name="Id",
            type="S",
        )
    ],
    hash_key="Id",
    read_capacity=1,
    write_capacity=1,
)

## EC2
eip = ec2.Eip("myeip")

security_group = ec2.SecurityGroup(
    "mysecuritygroup",
    ingress=[
        ec2.SecurityGroupIngressArgs(
            protocol="tcp", from_port=80, to_port=80, cidr_blocks=["0.0.0.0/0"]
        )
    ],
)

vpc = ec2.Vpc("myvpc", cidr_block="10.0.0.0/16")

igw = ec2.InternetGateway("myinternetgateway", vpc_id=vpc.id)

public_route_table = ec2.RouteTable(
    "myroutetable",
    routes=[ec2.RouteTableRouteArgs(cidr_block="0.0.0.0/0", gateway_id=igw.id)],
    vpc_id=vpc.id,
)

## ECR

repository = ecr.Repository("myrepository")

repository_policy = ecr.RepositoryPolicy(
    "myrepositorypolicy",
    repository=repository.id,
    policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "new policy",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": [
                        "ecr:GetDownloadUrlForLayer",
                        "ecr:BatchGetImage",
                        "ecr:BatchCheckLayerAvailability",
                        "ecr:PutImage",
                        "ecr:InitiateLayerUpload",
                        "ecr:UploadLayerPart",
                        "ecr:CompleteLayerUpload",
                        "ecr:DescribeRepositories",
                        "ecr:GetRepositoryPolicy",
                        "ecr:ListImages",
                        "ecr:DeleteRepository",
                        "ecr:BatchDeleteImage",
                        "ecr:SetRepositoryPolicy",
                        "ecr:DeleteRepositoryPolicy",
                    ],
                }
            ],
        }
    ),
)

lifecycle_policy = ecr.LifecyclePolicy(
    "mylifecyclepolicy",
    repository=repository.id,
    policy=json.dumps(
        {
            "rules": [
                {
                    "rulePriority": 1,
                    "description": "Expire images older than 14 days",
                    "selection": {
                        "tagStatus": "untagged",
                        "countType": "sinceImagePushed",
                        "countUnit": "days",
                        "countNumber": 14,
                    },
                    "action": {"type": "expire"},
                }
            ]
        }
    ),
)

## ECS

cluster = ecs.Cluster("mycluster")

role = iam.Role(
    "myrole",
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Principal": {"Service": "ec2.amazonaws.com"},
                    "Effect": "Allow",
                    "Sid": "",
                }
            ],
        }
    ),
)

role_policy = iam.RolePolicy(
    "myrolepolicy",
    role=role.id,
    policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [{"Action": ["ec2:Describe*"], "Effect": "Allow", "Resource": "*"}],
        }
    ),
)

policy = iam.Policy(
    "mypolicy",
    policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [{"Action": ["ec2:Describe*"], "Effect": "Allow", "Resource": "*"}],
        }
    ),
)

role_policy_attachment = iam.RolePolicyAttachment(
    "myrolepolicyattachment", role=role.id, policy_arn=policy.arn
)

user = iam.User("myuser")

group = iam.Group("mygroup")

## Kinesis
stream = kinesis.Stream("mystream", shard_count=1)

## SQS
queue = sqs.Queue("myqueue")

## SNS
topic = sns.Topic("mytopic")

topic_subscription = sns.TopicSubscription(
    "mytopicsubscription", topic=topic.arn, protocol="sqs", endpoint=queue.arn
)
```

