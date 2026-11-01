# HBnB Technical Architecture & Design Document

## 1. Introduction

This document serves as the comprehensive technical blueprint for the **HBnB** application. It details the system architecture, core domain models, layer interaction patterns, and execution flows for key application use cases. Designed following strict object-oriented and layered software design principles, this documentation guides the implementation phases to ensure high cohesion, low coupling, and maintainability.

---

## 2. High-Level Architecture

The HBnB application adheres to a 3-tier layered architecture decoupled by the **Facade Pattern**.

### Package Diagram

```mermaid
classDiagram
    namespace PresentationLayer {
        class APIEndpoints
        class Services
    }

    namespace BusinessLogicLayer {
        class HBnBFacade {
            <<Facade>>
        }
        class User
        class Place
        class Review
        class Amenity
    }

    namespace PersistenceLayer {
        class IPersistenceRepository {
            <<Interface>>
        }
    }

    %% Layer Communication Pathways via Facade Pattern
    APIEndpoints --> HBnBFacade : Communicates
    Services --> HBnBFacade : Communicates
    HBnBFacade --> User : Manages
    HBnBFacade --> Place : Manages
    HBnBFacade --> Review : Manages
    HBnBFacade --> Amenity : Manages
    HBnBFacade --> IPersistenceRepository : Accesses Data
```

### Layer Descriptions & Facade Pattern Overview

* **Presentation Layer:** Contains API endpoints and services. Handles user/client interaction by validating HTTP requests and formatting structured JSON responses. It has no direct connection to storage engines.
* **Business Logic Layer:** Encapsulates domain logic, entity definitions (`User`, `Place`, `Review`, `Amenity`), and business rules. It contains the `HBnBFacade`, which acts as the entry interface for presentation callers.
* **Persistence Layer:** Handles data storage and retrieval via repository patterns (`IPersistenceRepository`). Abstracts underlying storage mechanisms (in-memory or relational databases) from upper layers.
* **Facade Pattern Communication:** The `HBnBFacade` provides a unified entry point, isolating the Presentation Layer from internal entity instantiations and persistence operations.

---

## 3. Business Logic Layer

### Detailed Class Diagram

```mermaid
classDiagram
    class BaseModel {
        +UUID4 id
        +DateTime created_at
        +DateTime updated_at
        +save()
        +update(dict data)
    }

    class User {
        +String first_name
        +String last_name
        +String email
        +String password
        +Boolean is_admin
        +register()
        +update_profile()
    }

    class Place {
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +UUID4 owner_id
        +add_amenity(Amenity amenity)
        +add_review(Review review)
    }

    class Review {
        +String text
        +Int rating
        +UUID4 place_id
        +UUID4 user_id
        +validate()
    }

    class Amenity {
        +String name
        +String description
    }

    %% Generalization (Inheritance)
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    %% Associations & Multiplicity
    User "1" -- "0..*" Place : owns >
    User "1" -- "0..*" Review : writes >
    Place "1" -- "0..*" Review : receives >
    Place "0..*" -- "0..*" Amenity : features >
```

### Entity & Relationship Notes

* **`BaseModel`:** Abstract parent class containing core attributes shared across entities: unique identifier (`id` via UUID4) and audit timestamps (`created_at`, `updated_at`).
* **`User`:** Encapsulates user profile details and credentials. Holds a 1-to-many relationship with `Place` (as owner) and `Review` (as author).
* **`Place`:** Defines property listing parameters. Relates to `User` via `owner_id`, possesses a 1-to-many association with `Review`, and maintains a many-to-many relationship with `Amenity`.
* **`Review`:** Stores feedback and rating data, maintaining foreign reference links (`place_id`, `user_id`) to connect users and places.
* **`Amenity`:** Represents listing features or services (e.g., Wi-Fi, Pool) associated with places.

---

## 4. API Interaction Flow

### 1. User Registration (`POST /api/v1/users`)

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation Layer (API)
    participant Facade as Business Logic Layer (Facade)
    participant Repository as Persistence Layer (Repository)

    Client->>API: POST /api/v1/users (User Data JSON)
    API->>Facade: register_user(user_data)
    Facade->>Facade: Validate Email & Required Attributes
    Facade->>Repository: get_by_attribute("email", email)
    Repository-->>Facade: Return None (Email Available)
    Facade->>Facade: Instantiate User Entity
    Facade->>Repository: add(user_instance)
    Repository-->>Facade: Confirm Save Success
    Facade-->>API: Return User Entity
    API-->>Client: 201 Created (User DTO JSON)
```

* **Purpose & Flow:** Handles new user onboarding. The API delegates payload verification to `facade.register_user()`. The facade verifies email uniqueness, instantiates `User`, and instructs the repository to persist the object before returning HTTP 201.

---

### 2. Place Creation (`POST /api/v1/places`)

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation Layer (API)
    participant Facade as Business Logic Layer (Facade)
    participant Repository as Persistence Layer (Repository)

    Client->>API: POST /api/v1/places (Place Data JSON)
    API->>Facade: create_place(place_data)
    Facade->>Repository: get(owner_id)
    Repository-->>Facade: Return User Entity
    Facade->>Facade: Validate Attributes (Price, Latitude, Longitude)
    Facade->>Facade: Instantiate Place Entity
    Facade->>Repository: add(place_instance)
    Repository-->>Facade: Confirm Save Success
    Facade-->>API: Return Place Entity
    API-->>Client: 201 Created (Place DTO JSON)
```

* **Purpose & Flow:** Manages listing additions. The API sends details to `facade.create_place()`, which checks the persistence layer to confirm `owner_id` validity, verifies location and price constraints, saves the `Place` instance, and returns the response.

---

### 3. Review Submission (`POST /api/v1/places/{id}/reviews`)

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation Layer (API)
    participant Facade as Business Logic Layer (Facade)
    participant Repository as Persistence Layer (Repository)

    Client->>API: POST /api/v1/places/{id}/reviews (Review Data JSON)
    API->>Facade: create_review(place_id, review_data)
    Facade->>Repository: get(place_id)
    Repository-->>Facade: Return Place Entity
    Facade->>Facade: Validate Rating (1-5) & Review Text
    Facade->>Repository: add(review_instance)
    Repository-->>Facade: Confirm Save Success
    Facade-->>API: Return Review Entity
    API-->>Client: 201 Created (Review DTO JSON)
```

* **Purpose & Flow:** Processes feedback submissions. The facade confirms target `place_id` existence in storage, enforces rating limits (1–5 stars), generates the `Review` entity, and records it via the repository layer.

---

### 4. Fetching a List of Places (`GET /api/v1/places`)

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation Layer (API)
    participant Facade as Business Logic Layer (Facade)
    participant Repository as Persistence Layer (Repository)

    Client->>API: GET /api/v1/places (Query Parameters)
    API->>Facade: get_places(filters)
    Facade->>Repository: get_all()
    Repository-->>Facade: Return All Place Entities
    Facade->>Facade: Filter Places by Criteria (Price, Location, Amenities)
    Facade-->>API: Return Filtered Place Entities
    API-->>Client: 200 OK (Places Array JSON)
```

* **Purpose & Flow:** Executes place queries. The API passes search parameters to the facade, which retrieves stored entities from the persistence repository, executes filtering logic, and returns the formatted collection in a HTTP 200 JSON payload.
