# VaultRewards

A membership, virtual credit card, and real-time rewards SaaS platform.
Built on AWS as a hands-on DevOps training project.

## What It Does

- Member portal — Silver, Gold, Platinum tiers with virtual Visa/Mastercard
- Real-time points engine — points calculated per transaction via Lambda and SQS
- Notifications — email via SES, monthly PDF statements in S3
- Admin dashboard — member analytics, fraud flags, campaign performance

## Tech Stack

| Layer          | Technology                        |
|----------------|-----------------------------------|
| Infrastructure | Terraform                         |
| Container      | Docker + AWS ECR                  |
| Orchestration  | AWS EKS + Kubernetes              |
| GitOps         | ArgoCD                            |
| CI/CD          | Jenkins + GitHub Actions          |
| Database       | Aurora PostgreSQL                 |
| Cache          | ElastiCache Redis                 |
| Serverless     | Lambda + SQS + API Gateway        |
| Monitoring     | CloudWatch + Prometheus + Grafana |
| Security       | GuardDuty + WAF + Trivy           |

## Build Phases

- [x] Phase 1 — Network and Security Foundation
- [ ] Phase 2 — Infrastructure as Code (Terraform)
- [ ] Phase 3 — Containerisation
- [ ] Phase 4 — EKS and ArgoCD
- [ ] Phase 5 — CI/CD Pipeline
- [ ] Phase 6 — Data Layer and Serverless
- [ ] Phase 7 — Observability and DevSecOps
- [ ] Phase 8 — Cost Optimisation and HA
- [ ] Phase 9 — Go Live

## Author

Nikhil Reddy — Cloud Operations Analyst transitioning to DevOps Engineer
