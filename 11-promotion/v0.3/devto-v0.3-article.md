---
title: "What Comes After Docker Compose for Small Teams?"
published: false
description: "xtrape-capsule v0.3: a lightweight service governance experiment for small private deployments."
tags: opensource, devops, docker, selfhosted
canonical_url: 
cover_image: 
---

# What Comes After Docker Compose for Small Teams?

For many small teams, private deployments start with a very practical choice:

> Put the services into Docker Compose and make them run.

This is often the right decision. Docker Compose is simple, understandable, and easy to operate. For a small private deployment, it may be much more realistic than introducing a full Kubernetes cluster from day one.

But after the first few services are running, another set of problems slowly appears.

Docker Compose can start services, but it does not fully answer questions like:

- Which services are currently registered?
- Which node is a service running on?
- What version is deployed?
- Is the service healthy at the business level?
- How should service metadata be reported?
- How can a small team manage services without exposing an admin API on every node?
- At what point does the team really need Kubernetes?

This is the gap I am exploring with **xtrape-capsule**.

## The Problem: Running Is Not the Same as Governing

A container being up does not always mean the service is usable.

In many private or self-hosted deployments, teams need a minimal operational layer around their services:

- service identity
- service registration
- runtime status
- version information
- node relationship
- centralized visibility
- basic governance operations

These are not always container-level concerns. They are service-level concerns.

This distinction matters.

A container platform manages containers. A service governance layer should understand services as operational units.

## Why Not Just Use Kubernetes?

Kubernetes is powerful. It solves many real problems around orchestration, scaling, service discovery, scheduling, and deployment automation.

But for small private deployments, it can also be too much.

A team may only have:

- 1-3 nodes
- 5-20 services
- limited operations capacity
- customer-private environments
- strict network exposure requirements
- no dedicated platform engineering team

In such environments, the first need is often not full orchestration.

The first need is visibility and control:

> What is running, where is it running, and how do we manage it safely?

This is why I think there is room for a lightweight layer before Kubernetes.

## The Direction: Lightweight Service Governance

xtrape-capsule is an open-source experiment around this idea.

The current model has three main concepts:

### opstage

The central operations platform.

It provides the management surface for services and nodes.

### ophub

The node-side hub / agent component.

It is responsible for connecting node-side runtime information to opstage. A key design preference is that the node side can actively communicate with the platform, instead of requiring every node to expose a management API.

### capsule-service

A lightweight service that can be registered, observed, and managed through the capsule model.

The goal is not to replace Docker Compose, Portainer, or Kubernetes.

The goal is to define a smaller governance layer for teams that are not ready for Kubernetes, but have already outgrown “just run a few containers”.

## Why Avoid Exposing Management APIs Everywhere?

In private deployments, every exposed management endpoint becomes part of the attack surface.

If each service or node exposes its own admin API, the operational model becomes harder to secure:

- more endpoints to protect
- more credentials to manage
- more network rules to maintain
- more ways to misconfigure access
- more places where a service-specific admin UI may leak

For small teams, centralized governance with node-side outbound communication can be safer and easier to operate.

This is one of the main reasons xtrape-capsule is moving toward an ophub-based model.

## What Is New in v0.3?

v0.3 is still early. It is not a production-ready platform.

The focus of this release is architectural review around:

- the opstage / ophub / capsule-service model
- lightweight service registration
- private deployment assumptions
- agent/hub-based node governance
- the boundary between container management and service governance

The project is open source and currently in public review.

Repository:

```text
https://github.com/xtrape-com/xtrape-capsule-ce
```

## What I Am Looking For

I am especially interested in feedback on these questions:

1. Does the “service governance before Kubernetes” problem feel real?
2. How do you currently manage small private services after Docker Compose?
3. Would an agent / hub model make sense in your private deployment environment?
4. What would you expect from a minimal useful version?
5. Where should the boundary be between xtrape-capsule, Portainer, Docker Compose, and Kubernetes?

## Closing Thought

For small teams, the path should not always be:

> Docker Compose today, Kubernetes tomorrow.

There may be an intermediate layer:

> Docker Compose for running services, plus lightweight governance for understanding and managing them.

That is the direction xtrape-capsule is exploring.

If this problem matches something you have experienced, I would appreciate your feedback.
