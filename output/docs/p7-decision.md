# P7. Decision Guide

## 1. When to Use

## P7: Decision Guide - When to Use This Framework

This standardized, cloud-native framework is specifically designed for scenarios demanding high performance, resilience, and operational excellence. It should be the default choice when the following conditions or requirements are met:

1.  **High-Volume Transactional Systems:** For APIs expected to handle a large number of requests per second (e.g., thousands to millions), such as payment gateways, real-time trading platforms, e-commerce checkout services, or high-frequency data ingestion points.
2.  **Low-Latency Criticality:** When API response times are a critical business requirement, impacting user experience, system integration, or real-time decision-making (e.g., sub-100ms latency targets).
3.  **New API Development (Greenfield):** As the foundational framework for all new API services that are anticipated to grow in scale and complexity, ensuring consistency and best practices from inception.
4.  **Modernizing Legacy APIs:** For replacing existing monolithic or underperforming APIs that struggle with scalability, resilience, or maintainability, and are hindering business growth or operational stability.
5.  **Microservices Architectures:** When building or expanding a microservices ecosystem, this framework provides the standardized patterns and tooling for inter-service communication and external API exposure.
6.  **Cloud-First or Cloud-Native Strategy:** For organizations committed to leveraging public cloud capabilities (e.g., AWS, Azure, GCP) for infrastructure, managed services, and platform features to maximize scalability and operational efficiency.
7.  **Standardization and Governance Initiatives:** When the enterprise aims to reduce architectural sprawl, promote consistent development practices, and ensure a baseline level of quality, security, and performance across all API services.
8.  **Resilience and Fault Tolerance Requirements:** For business-critical APIs where downtime or performance degradation has significant financial or reputational impact, necessitating robust fault tolerance, disaster recovery, and self-healing capabilities.
9.  **Data-Intensive Applications:** When APIs are serving or processing large volumes of data, requiring efficient data access patterns, caching strategies, and scalable data stores.
10. **Cost-Sensitive at Scale:** When the long-term operational cost of running high-volume services needs to be optimized through efficient resource utilization, automation, and cloud-native cost management practices.

## 2. When NOT to Use

## P7: Decision Guide - When NOT to Use This Framework

While powerful, this framework is not a universal solution. Applying it indiscriminately can introduce unnecessary complexity, cost, and overhead. Avoid using this framework in the following scenarios:

1.  **Low-Traffic, Internal-Only APIs:** For simple internal APIs with minimal performance, scalability, or resilience requirements (e.g., administrative tools, internal data lookups with infrequent access), the overhead of implementing and operating a high-throughput framework is not justified.
2.  **Batch Processing or Long-Running Jobs:** Workloads that are inherently asynchronous, non-interactive, and do not require immediate responses (e.g., nightly data processing, large file conversions, report generation) are better suited for dedicated batch processing or workflow orchestration services.
3.  **Strict On-Premise or Hybrid Cloud Requirements:** If there are hard constraints against using public cloud infrastructure or specific cloud-native services, or if the environment is predominantly on-premise without a clear path to cloud adoption, the "cloud-native" aspect of the framework becomes a significant impediment.
4.  **Rapid Prototyping or Initial MVPs (unless high-throughput is the core MVP):** The initial setup and configuration of a robust, high-throughput framework can be time-consuming. For early-stage prototypes or MVPs where the primary goal is rapid validation of business value, a simpler, less opinionated approach might be more appropriate, unless the MVP *itself* is a high-throughput service.
5.  **Monolithic Applications Without Decomposition Plans:** Attempting to force a high-throughput, cloud-native API framework onto a tightly coupled monolithic application without a clear, funded strategy for decomposition into microservices will likely lead to increased complexity without realizing the benefits.
6.  **Highly Specialized Niche Services:** For services with unique, non-standard technical requirements that fundamentally conflict with the framework's "opinionated technology choices" or architectural patterns, a custom approach might be more efficient than trying to force a square peg into a round hole.
7.  **Small Teams with Limited Cloud-Native/Distributed Systems Expertise:** The operational complexity of managing high-throughput, distributed, cloud-native systems requires a certain level of skill and maturity within development and operations teams. Without this expertise, adoption can lead to significant operational challenges and project delays.
8.  **Extreme Budget Constraints for Infrastructure:** While the framework aims for operational efficiency, achieving extreme performance and resilience often involves higher infrastructure costs (e.g., multi-region deployments, premium managed services). If the budget cannot support these costs, a more constrained approach may be necessary.
9.  **Simple CRUD APIs with Low Expected Growth:** For straightforward Create, Read, Update, Delete (CRUD) APIs that are not expected to experience significant traffic growth or require advanced resilience, the framework's overhead might be excessive.