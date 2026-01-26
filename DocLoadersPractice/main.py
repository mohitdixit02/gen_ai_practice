from docLoader import DocLoader

if __name__ == "__main__":
    print("\n\n--- Document Loader Practice 📄 ---\n")
    while True:
        print("Available Document Loaders:")
        print("1. Text Loader")
        print("2. PDF Loader")
        print("3. Directory Loader")
        print("4. Web Page Loader")
        print("5. CSV Loader")
        print("6. Exit")
        choice = input("Select a loader (1-5): ")
        if choice == '6':
            print("👋 Exiting Document Loader Practice!")
            break
        doc_loader = DocLoader()
        doc_loader.load(loader_type=choice)