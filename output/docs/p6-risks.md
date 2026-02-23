# P6. Risks & Anti-patterns

## 1. Risk & Anti-pattern

## P6: Risks and Anti-patterns

Adopting a high-throughput, low-latency API framework, while beneficial, introduces specific risks and can lead to common anti-patterns if not carefully managed.

### Key Risks

1.  **Over-engineering/Premature Optimization:** The directive for "high-throughput, low-latency" can lead teams to build overly complex solutions for anticipated scale that isn't yet realized, increasing development cost, time-to-market, and operational burden without immediate benefit.
2.  **Vendor Lock-in:** While "cloud-native" and "opinionated technology choices" promote standardization and leverage cloud strengths, they can create deep dependencies on a specific cloud provider's services (e.g., managed databases, message queues, serverless functions), making multi-cloud strategies or future migrations difficult and costly.
3.  **Complexity Creep:** Implementing advanced architectural patterns (e.g., event-driven architectures, distributed tracing, service meshes) for resilience and scalability inherently adds operational complexity. Without robust automation, skilled teams, and mature processes, this can negate "operational efficiency."
4.  **Inadequate Observability:** High-throughput, distributed systems are notoriously difficult to debug and monitor without comprehensive logging, metrics, and tracing. A lack of robust observability can severely impact "operational efficiency" and the ability to ensure "resilience" and "low-latency."
5.  **Security Gaps in Distributed Systems:** The speed and scale of development in a distributed, cloud-native environment can sometimes lead to overlooking critical security best practices, especially concerning API authentication/authorization, data encryption in transit/at rest, and vulnerability management across numerous components.
6.  **Data Consistency Challenges:** Achieving high scalability often involves relaxing strong data consistency guarantees (e.g., favoring eventual consistency). Misunderstanding or misapplying consistency models can lead to data integrity issues or incorrect business outcomes.
7.  **Skill Gap and Onboarding Overhead:** The "opinionated technology choices" and advanced architectural patterns may require specialized skills (e.g., Kubernetes, Kafka, specific cloud services, distributed systems design) that are not uniformly present across all development and operations teams, hindering adoption and increasing project risk.
8.  **Cost Overruns at Scale:** Cloud-native services, especially when provisioned for high throughput and resilience (e.g., multi-AZ/region deployments, premium tiers, extensive caching), can become very expensive if not continuously monitored, optimized, and governed for cost efficiency.

### Common Anti-patterns

1.  **Monolithic API Gateway:** Routing all traffic through a single, non-scalable, or overly complex API gateway that becomes a bottleneck or single point of failure.
2.  **Synchronous Inter-service Communication:** Over-reliance on synchronous HTTP calls between microservices, creating tight coupling, increasing latency, and propagating failures across the system.
3.  **Lack of Circuit Breakers/Bulkheads:** Failing to implement resilience patterns that isolate failures, leading to cascading outages when a downstream service becomes unavailable or slow.
4.  **Ignoring Idempotency:** Designing APIs that perform non-idempotent operations without proper handling for retries, leading to duplicate processing of requests (e.g., double payments).
5.  **Manual Scaling:** Relying on manual intervention for scaling high-throughput services, which is unsustainable and reactive, failing to meet dynamic demand.
6.  **"Big Ball of Mud" Microservices:** Decomposing services without clear domain boundaries, leading to tightly coupled, distributed monoliths that are harder to develop, deploy, and operate than a traditional monolith.
7.  **Chatty APIs:** Designing APIs that require multiple round trips to achieve a single logical operation, significantly increasing network latency and client-side complexity.
8.  **Ignoring API Versioning:** Introducing breaking changes to APIs without proper versioning strategies, causing disruption for consumers and hindering independent evolution of services.

## 2. Trade-offs (ได้อย่าง เสียอย่าง)

## P6: Trade-offs

Implementing a standardized, cloud-native framework for high-throughput, low-latency API services necessitates careful consideration of inherent trade-offs. Decisions made here will impact development velocity, operational cost, and long-term maintainability.

1.  **Standardization vs. Flexibility:**
    *   **Pro-Standardization:** "Opinionated technology choices" and "architectural patterns" provide consistency, accelerate onboarding, reduce architectural sprawl, and simplify operations. This directly supports "operational efficiency."
    *   **Con-Flexibility:** It inherently limits technology freedom for specific niche use cases or developer preferences, potentially stifling innovation or requiring workarounds for non-standard requirements.

2.  **Performance (High-throughput, Low-latency) vs. Cost:**
    *   **Pro-Performance:** Achieving extreme performance often requires more expensive cloud resources (e.g., dedicated instances, premium managed services, advanced caching layers, multi-region deployments) and significant engineering effort for optimization.
    *   **Con-Cost:** This can lead to higher infrastructure and operational costs. Balancing the required performance with a sustainable budget is crucial.

3.  **Resilience vs. Complexity:**
    *   **Pro-Resilience:** Building highly resilient systems (e.g., multi-AZ/region deployments, active-active patterns, sophisticated retry/circuit breaker logic, robust disaster recovery) is fundamental to the directive.
    *   **Con-Complexity:** These patterns inherently add significant complexity to design, development, testing, and operations. The more resilient a system, the more moving parts and failure modes to consider.

4.  **Scalability vs. Data Consistency:**
    *   **Pro-Scalability:** To achieve "high-throughput," systems often adopt eventual consistency models (e.g., using asynchronous messaging, distributed databases with relaxed consistency) to avoid bottlenecks associated with strong consistency.
    *   **Con-Consistency:** This can be a trade-off against immediate, strong data consistency, which might be critical for certain business transactions. Understanding and managing consistency models is paramount.

5.  **Time-to-Market vs. Robustness/Maturity:**
    *   **Pro-Time-to-Market:** A standardized framework can accelerate initial development by providing pre-built components and patterns.
    *   **Con-Robustness:** Rushing to market without fully implementing and testing all aspects of resilience, observability, and security in a high-throughput environment can lead to significant technical debt and operational instability down the line.

6.  **Cloud-Native Integration vs. Portability:**
    *   **Pro-Cloud-Native:** Deep integration with cloud-native services (e.g., serverless, managed databases, message queues) maximizes "operational efficiency," leverages cloud provider scale, and reduces undifferentiated heavy lifting.
    *   **Con-Portability:** This deep integration reduces portability to other cloud providers or on-premise environments, increasing the effort required for migration.

7.  **Operational Efficiency vs. Initial Development Effort:**
    *   **Pro-Operational Efficiency:** Implementing robust CI/CD pipelines, comprehensive observability, automated scaling, and self-healing capabilities upfront significantly improves long-term "operational efficiency."
    *   **Con-Initial Effort:** This requires a substantial upfront investment in tooling, infrastructure-as-code, and process development, which can slow down initial feature delivery.

8.  **Developer Autonomy vs. Governance/Standardization:**
    *   **Pro-Autonomy:** Microservices architectures, often associated with high-throughput APIs, can empower small, autonomous teams.
    *   **Con-Governance:** The "standardized framework" and "opinionated technology choices" impose certain constraints and governance overhead to ensure consistency, security, and maintainability across the enterprise, potentially limiting individual team choices.