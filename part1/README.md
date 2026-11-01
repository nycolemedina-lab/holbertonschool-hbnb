# HBnB High-Level Package Diagram & Architecture Documentation

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
