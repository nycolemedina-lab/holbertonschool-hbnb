# HBnB - High-Level Architecture & Package Structure

This project follows a 3-Tier Layered Architecture decoupled by the **Facade Pattern** to maintain separation of concerns, high cohesion, and low coupling.

---

## 1. High-Level Package Diagram

```mermaid
classDiagram
    namespace PresentationLayer {
        class APIEndpoints {
            +UserRoutes
            +PlaceRoutes
            +ReviewRoutes
            +AmenityRoutes
        }
    }

    namespace BusinessLogicLayer {
        class HBnBFacade {
            <<Facade>>
            +create_user(data)
            +get_user(user_id)
            +create_place(data)
            +get_place(place_id)
            +create_review(data)
            +add_amenity(data)
        }
        class User {
            +String id
            +String email
            +String first_name
            +String last_name
        }
        class Place {
            +String id
            +String title
            +Float price
            +Float latitude
            +Float longitude
        }
        class Review {
            +String id
            +String text
            +Int rating
        }
        class Amenity {
            +String id
            +String name
        }
    }

    namespace PersistenceLayer {
        class IPersistenceRepository {
            <<Interface>>
            +add(entity)
            +get(entity_id)
            +get_all()
            +update(entity)
            +delete(entity_id)
        }
        class InMemoryRepository {
            -dict data
        }
        class DBRepository {
            -Session db_session
        }
    }

    %% Layer Interactions & Communication Pathways
    APIEndpoints --> HBnBFacade : Delegates Requests
    HBnBFacade --> User : Manages
    HBnBFacade --> Place : Manages
    HBnBFacade --> Review : Manages
    HBnBFacade --> Amenity : Manages
    HBnBFacade --> IPersistenceRepository : Executes Storage Operations
    InMemoryRepository ..|> IPersistenceRepository : Implements
    DBRepository ..|> IPersistenceRepository : Implements
```

---

## 2. Layer Architecture Overview

| Layer | Primary Components | Key Responsibilities |
| :--- | :--- | :--- |
| **Presentation Layer** | API Endpoints, Controllers | Receives HTTP requests, validates input DTOs, routes requests to the Facade, and returns structured JSON responses. |
| **Business Logic Layer** | `HBnBFacade`, Core Models (`User`, `Place`, `Review`, `Amenity`) | Enforces domain rules, manages model state/relationships, and coordinates entity operations through the Facade. |
| **Persistence Layer** | `IPersistenceRepository`, `InMemoryRepository`, `DBRepository` | Abstracted storage interface managing persistent operations (CRUD), allowing transparent switching between memory and SQL databases. |

---

## 3. Facade Pattern Design

The **`HBnBFacade`** serves as the single entry point for all API operations interacting with the business logic and persistence tiers:

* **Unified API Interface:** Isolates endpoints from underlying model instantiation logic or repository calls.
* **Decoupled Architecture:** Internal refactoring of entity methods or persistence engines requires zero changes to the API controllers.
* **Execution Pathway:**
  1. `APIEndpoints` receives request payload $\rightarrow$ calls `HBnBFacade` method (e.g., `facade.create_place(data)`).
  2. `HBnBFacade` validates attributes, instantiates `Place`, and invokes `IPersistenceRepository.add(place)`.
  3. Result object is passed back to `APIEndpoints` to construct the HTTP response.
