import sys
from src.model.book import Book
from src.model.member import Member
from src.model.loan import Loan
from src.services.catalog import Catalog
from src.services.persistence import PersistenceService

def main():
    # --- 1. Setup Services ---
    persistence = PersistenceService()
    data_file = "data/library_data.json"
    
    print("=== Starting Library System ===")

    # --- 2. Load Data ---
    # We load existing items and members from the JSON file
    loaded_items, loaded_members = persistence.load_library_state(data_file)
    
    # Initialize the catalog with the loaded items
    catalog = Catalog(initial_items=loaded_items)
    
    # Simple check to see if we have members, otherwise create a default one
    if not loaded_members:
        print("No members found. Creating default admin member.")
        current_member = Member("LIB001", "Admin User")
        loaded_members.append(current_member)
    else:
        current_member = loaded_members[0]
        print(f"Welcome back, {current_member.member_id}")

# In main.py, replace the "Interaction" and "Save" sections with this:

    # --- 3. Interaction (Simulation) ---
    print("\n--- Current Catalog Report ---")
    print(catalog.report())

    # Check/Add Book Logic... (Keep your existing check here)
    test_isbn = "9780307278449"
    search_results = catalog.search("Bluest Eye")
    
    current_book = None
    if not search_results:
        print("\n[Action] Adding new book to catalog...")
        current_book = Book("The Bluest Eye", "Toni Morrison", 1970, test_isbn, "Literature", 101)
        catalog.add_item(current_book)
    else:
        print("\n[Action] Book already exists in catalog.")
        current_book = search_results[0]

    if current_book and current_book.is_available:
        print(f"[Action] Checking out '{current_book.title}' to generate fines...")
        current_book.mark_checked_out()

    print("\n--- Generating Fine Revenue Report ---")
    report_file = "data/fine_revenue_report.csv"
    persistence.export_fine_report(report_file, catalog, loaded_members)

    print("\n--- Saving System State ---")
    persistence.save_library_state(data_file, catalog, loaded_members)
    print("=== System Shutdown Complete ===")

if __name__ == "__main__":
    main()