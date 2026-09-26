# SustratIO

SustratIO is an open-source ([see License](./LICENSE)) environment designed to
monitor, track, and notify users about soil quality in real time. By decoupling
infrastructure configuration from domain logic, the platform serves as a
flexible baseline that organizations can host and tailor to their agricultural
needs.

## System Architecture

The project follows a *Domain-Driven Design* under a *Hexagonal Architecture*
in which the layers are clearly differentiated:

- **Domain Layer**: Contains interfaces, types and validation functions that
define core business logic.
- **Infrastructure Layer**: Implements external APIs communication, data
mappers and HTTP clients.
- **Application Layer**: Embodies business use cases with their respective
business rules.
  - *Primary Driving Adapters*: These are the entry points for external
  communication, such as REST APIs or message queues.
  - *Secondary Driven Adapters*: These are the exit points for external
  communication, such as database clients or third-party services.
- **Field Layer**: Edge devices equipped with biomarkers, soil temperature
sensors, and Capacitive Moisture sensors that send readings to a dispatcher.

### Folder Structure

> **Note**: The following folder structure might evolve as the project matures,
> but the core principles of separation of concerns and modularity will remain
> intact.

```plaintext
src/
├── application/         # Business use cases and Data Transfer Objects (DTOs)
│   ├── dtos/            # Data Transfer Objects (DTOs) for use cases
│   └── use_cases/       # Use cases implementing business rules
│
├── domain/
│   ├── exceptions/      # Exceptions and error handling for domain logic
│   ├── models/          # Models representing core business entities
│   └── ports/           # Interfaces for external dependencies
│
└── infrastructure/      # Outer layer for external services and APIs
    ├── adapters/        # Adapters for external services and APIs
    │   ├── auth/        # Authentication and authorization adapters
    │   └── persistence/ # Persistence adapters for database interactions
    │
    └── entrypoints/     # Entry points for external communication
        └── api/         # API endpoints for the application
```

## Configuration Boundaries

Because SustratIO is a self-hosted platform, configuration is strictly divided
into two tiers:

- **Source Code & Environment**: Handles all deployment requirements and
outer-hexagon connections. This includes database URIs, messaging brokers
(e.g., RabbitMQ), worker ports, CORS allowed origins, and external Auth/Cache
providers.
- **Back-Office UI**: Manages runtime domain data, role assignments, and
user-specific settings. No infrastructure configuration leaks into the UI.

## User Roles & Permissions

The system operates on a strict Permission-Based Access Control (PBAC) model
and a Attribute-Based Access Control (ABAC) to ensure data integrity and
ownership across the field and the dashboard:

- **Administrator**: Holds unrestricted access to all system functions and
serves as the ultimate fallback for unacknowledged critical alerts.
- **Farm Owner**: Defines the global catalog. They create new Crop types,
establish global safety thresholds for those crops, and manage the lifecycle of
plots (registering and archiving).
- **Farm Manager**: Oversees daily field operations. They register new plots,
assign existing Crop profiles to them, and are the primary recipients of
real-time soil alerts. They hold the authority to acknowledge and dismiss
active alerts.
- **Field Technician**: Manages the hardware layer. They are scoped exclusively
to registering new edge devices and sensors (e.g., soil moisture, temperature)
and binding them to specific plots.
- **Read-Only Auditor**: Reserved for external agricultural inspectors, organic
certification bodies, or financial stakeholders who need to review historical
soil telemetry and compliance without modifying thresholds or hardware
bindings.

## The Operational Workflow

- **System Setup**: The platform is deployed using environment variables to
connect the backend to the chosen database and message brokers.
- **Domain Definition**: The Farm Owner logs into the back-office to establish
Crop profiles and global environmental thresholds.
- **Field Provisioning**: The Farm Manager maps out new plots and assigns the
appropriate crops.
- **Hardware Deployment**: The Field Technician registers the physical sensors
and logically binds them to the Manager's plots.
- **Monitoring & Alerting**: Telemetry flows into the system. If soil
parameters breach the global crop thresholds, an alert is dispatched to the
Farm Manager. If left unacknowledged, it escalates to the Farm Owner and, if
still unacknowledged, to the Administrator.
