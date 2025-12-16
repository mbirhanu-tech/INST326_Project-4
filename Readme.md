1. Technical Documentation


Architecture Overview and Design Decisions
The system follows a Service-Oriented Architecture (SOA) approach, strictly separating data models, business logic, and data persistence.


Layer 1: The Model Layer (src/model)


Design Decision: We used an Abstract Base Class (LibraryItem) to define the core interface for all library items.


Rationale: This ensures that every item (Book, DVD, EBook) guarantees specific behaviors (like calculate_loan_period and compute_fine). It allows the Catalog to treat all items uniformly (Polymorphism), simplifying the code significantly.


Layer 2: The Service Layer (src/services)


Design Decision: We separated the Catalog (in-memory management) from the PersistenceService (file I/O).


Rationale: This separation of concerns allows us to change how we save data (e.g., switching from JSON to a database later) without rewriting the core business logic of the Catalog.


Layer 3: The Utility Layer (src/utils)


Design Decision: Common validation logic (like validate_isbn) was placed in a standalone utility module.


Rationale: These pure functions can be reused anywhere in the application or by external scripts without needing to instantiate complex objects.


Key Design Choices
Polymorphism for Fines: Instead of a giant if/else block checking for item types, each class knows its own fine rate. A DVD calculates its own fine ($1.00/day) differently than a Book ($0.25/day).


JSON for Persistence: We chose JSON for state storage because it natively supports nested data structures (like lists of items) and is human-readable for debugging.


Dependency Injection: The Catalog does not load its own data; it accepts a list of items (initial_items) in its constructor. This makes testing easier because we can inject "fake" items during unit tests.




API / Interface Descriptions
Catalog.add_item(item: LibraryItem):


Accepts any object inheriting from LibraryItem.


Raises TypeError if the object is invalid.


Raises ValueError if the call number already exists.


LibraryItem.compute_fine(days_late: int) -> float:


Abstract method that must be implemented by subclasses.


Returns the monetary fine amount based on the specific item type's policy.


PersistenceService.save_library_state(file_path, catalog, members):


Serializes the entire system state into a JSON object and writes it to disk safely using a context manager.


Known Limitations & Future Enhancements
Limitation: The current system simulates "overdue" items by checking out an item and assuming a fixed number of days late. It does not yet have a full Loan object tracking real dates.


Limitation: The Member class is currently basic; it does not track history or accrued fines across sessions.


Future Enhancement: Implement a Loan class that links a Member to a LibraryItem with specific start_date and due_date fields.


Future Enhancement: Add a user interface (CLI or GUI) to allow librarians to interact with the system without editing code.


2. Testing Documentation


Testing Strategy Explanation
We employed a "pyramid" testing strategy, focusing heavily on robust Unit Tests for individual components and supplementing them with Integration and System tests to verify workflows.


Tooling: We used Python's standard unittest framework because it requires no external dependencies and offers built-in discovery.


Isolation: All tests use setUp and tearDown methods to create temporary files (data/test_temp...), ensuring that running tests never corrupts the actual production data.


Coverage Rationale (What we test and why)
Persistence Service (Unit Tests):


Why: File I/O is the most error-prone part of any application (missing files, bad permissions).


What: We test saving/loading valid data, handling missing files (returning empty lists instead of crashing), and handling corrupted JSON (graceful failure).


Polymorphism (Integration Tests):


Why: The core feature of Project 4 is handling different item types correctly.


What: We test that DVDs and Books return different values for compute_fine and calculate_loan_period even when treated as generic items in the Catalog.


Save/Load Cycle (System Tests):


Why: To answer the "Charter Question" (can we track fines across sessions?).


What: We simulate a full user session: adding a book, checking it out, saving, restarting, and verifying the book is still checked out.


How to Run the Test Suite
To execute the comprehensive test suite, navigate to the project root directory (project_4/) and run:
python -m unittest discover tests


This command automatically finds all files matching test_*.py in the tests/ folder and runs them.


Test Results Summary
Total Tests: 12 (approximate, depending on final count)


Status: All tests PASS.


Key Validations:


* Data persistence correctly saves/loads library state. 
* Polymorphic fine calculation works for Books vs. DVDs. 
* System recovers gracefully from missing or corrupt data files.
* CSV data import correctly populates the catalog.