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

    %% Relationships and Layer Interactions
    APIEndpoints --> HBnBFacade : Calls API Methods
    HBnBFacade --> User : Instantiates & Manages
    HBnBFacade --> Place : Instantiates & Manages
    HBnBFacade --> Review : Instantiates & Manages
    HBnBFacade --> Amenity : Instantiates & Manages
    HBnBFacade --> IPersistenceRepository : Executes Storage CRUD Operations
    InMemoryRepository ..|> IPersistenceRepository : Implements
    DBRepository ..|> IPersistenceRepository : Implements
