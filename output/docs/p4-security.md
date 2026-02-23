# P4. Security & NFR

## 1. Built-in Security Control

### Built-in Security Controls for High TPS API Services

Security is a foundational pillar, integrated throughout the design and operational lifecycle. This framework emphasizes a defense-in-depth strategy, leveraging cloud-native security capabilities.

**1. Identity and Access Management (IAM):**
*   **Least Privilege Principle:** All users, roles, and service accounts are granted only the minimum permissions required to perform their functions.
*   **Role-Based Access Control (RBAC):** Granular access control for cloud resources (e.g., AWS IAM, GCP IAM) and Kubernetes (K8s RBAC).
*   **Multi-Factor Authentication (MFA):** Enforced for all administrative and privileged access.
*   **Temporary Credentials:** Utilize short-lived credentials for programmatic access where possible.
*   **Service Account Isolation:** Dedicated Kubernetes service accounts for each microservice with minimal permissions.

**2. Network Security:**
*   **VPC Segmentation:** Logical isolation of environments (e.g., production, staging, development) and tiers (e.g., web, application, database) using subnets and routing tables.
*   **Security Groups/Network ACLs:** Strict ingress/egress rules to control traffic flow at the instance/interface level.
*   **Web Application Firewall (WAF):** Deployed at the API Gateway/Load Balancer to protect against common web exploits (e.g., OWASP Top 10) and DDoS attacks.
*   **DDoS Protection:** Leverage cloud provider's native DDoS mitigation services (e.g., AWS Shield Advanced, GCP Cloud Armor).


## 2. NFR Baseline



## 3. Observability

