Advanced DevOps In-House Technical
Challenge

Overview
This challenge is designed to simulate a real-world DevOps + backend system scenario
where you are responsible for:
● Building a backend service from scratch
● Handling real-time (simulated) data ingestion
● Designing storage and APIs
● Implementing CI/CD
● Deploying to a live environment
You are expected to make architectural decisions, justify trade-offs, and implement a
working system under time constraints.

Scenario
You are working on a smart city traffic monitoring system.
Your system must:
1. Ingest traffic congestion data in near real-time
2. Store the data efficiently
3. Expose APIs to retrieve and monitor the data
4. Automatically test and deploy using CI/CD
5. Run reliably in a production-like environment
⚠️ You will NOT be given any starter code. You must build everything from scratch.

Functional Requirements

1. Data Ingestion (Simulated Real-Time)
You must simulate incoming traffic data.
Each data point should include fields like:
● timestamp
● location_id (string or numeric)
● vehicle_count
● average_speed
● congestion_level (low / medium / high)
Requirements
● Create a script or process that continuously generates data (e.g., every 1–5 seconds)
● The backend must be able to receive this data via an API endpoint
Example:
POST /traffic

2. Backend Service (FastAPI)
Build a backend service using FastAPI.
Required APIs
● POST /traffic → ingest data
● GET /traffic → fetch recent traffic data
● GET /health → health check
Expectations
● Proper request validation
● Clean API design
● Error handling
3. Database Design
You may choose any database (SQL or NoSQL).

Requirements
● Store incoming traffic data
● Support efficient querying for recent data
● Handle frequent writes
You must justify:
● Why you chose this database
● Trade-offs (e.g., consistency vs performance)
4. Containerization
Dockerize your application.
Requirements
● Create a working Dockerfile
● Optimize for:
○ small image size
○ build speed
● Use best practices:
○ .dockerignore
○ non-root user (optional but strong signal)
5. CI/CD Pipeline (GitHub Actions)
Set up a CI/CD pipeline using GitHub Actions.
Pipeline must:
● Trigger on push to main
● Install dependencies
● Run tests
● Build Docker image
● Deploy to Render
You must handle:
● Secrets securely (API keys, tokens)
● Image tagging/versioning

6. Deployment (Render)
Deploy your service to Render
Requirements
● Service must be publicly accessible
● APIs should be testable via URL
● Deployment must be automated via CI/CD

Non-Functional Requirements (Important)
1. Scalability Considerations
Assume:
The system may receive 1000+ requests per second in the future
Be prepared to explain:
● How your system would scale
● Bottlenecks in your design
2. Reliability
Your system should:
● Not crash on bad input
● Handle failures gracefully
3. Observability
You should include:
● Basic logging
● Ability to debug failures
4. Security
● No hardcoded secrets
● Use environment variables

● Validate inputs

Hidden Complexity (Intentional)
You are expected to think about:
● High write throughput
● Data consistency
● API performance
● Deployment failures
● Stateless vs stateful design

Bonus (If Time Permits)
● Add filtering (e.g., by location or congestion level)
● Add rate limiting
● Add basic monitoring or metrics

Evaluation Criteria
We will evaluate based on:
1. System Design Thinking
● Clear architecture decisions
● Ability to explain trade-offs
2. DevOps Skills
● CI/CD pipeline quality
● Deployment automation
3. Code Quality
● Structure and readability
● API design
4. Problem Solving
● How you handle ambiguity

● How you debug issues
5. Communication
● Ability to explain decisions clearly

Important Notes
● You may use any documentation or online resources
● You are encouraged to think out loud while working
● Focus on correctness, clarity, and reasoning over completeness

Final Deliverable
By the end of the session, you should have:
● A GitHub repository with your code
● A working CI/CD pipeline
● A deployed live API on Render
● A brief explanation of your architecture and decisions