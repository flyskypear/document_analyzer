from analyzer.argparser import parser
from analyzer.analyzer import DocumentAnalyzer 
import shutil

if __name__ == '__main__':

    print("Welcome to Document Analyzer!")

    args = parser.parse_args()

    data = args.data
    chunks = args.chunks
    chunk_overlap = args.chunk_overlap
    num_chunks = args.num_chunks
    text_model = args.text_model
    model = args.model
    base_url = args.base_url
    api_key = args.api_key
    persist_directory = args.persist_directory
    temperature = args.temperature
    reset = args.reset
    source = args.include_sources
    additional_data = args.add_data

    analyzer = DocumentAnalyzer(
        model=model,
        api_key=api_key,
        api_url=base_url,
        text_model=text_model,
        chunk_size=chunks,
        chunk_overlap=chunk_overlap,
        num_chunks=num_chunks,
        persist_directory=persist_directory,
        temperature=temperature
    )

    if analyzer.vectorstore_exists():
        if reset:
            print(f"{persist_directory} already exists. It will be deleted. " \
                  "Please confirm by entering y, anything else will exit the program.")
            confirm = input("Confirm deletion (y/n): ")
            if confirm.lower() != 'y':
                print("Exiting program.")
                exit(0)
            shutil.rmtree(persist_directory)
        else:
            print(f"{persist_directory} already exists. Loading existing vectorstore. " \
                  "To re-create it, delete the existing vectorstore directory or pass the -r or --reset option.")
    else:
        reset = True

    vectorstore = analyzer.create_vectorstore()

    def _add_documents(dirs, vectorstore):
        files = []
        for dir in dirs:
            files.extend(analyzer.get_file_paths(dir))
        documents = analyzer.parse_files(files)
        analyzer.add_documents(documents, vectorstore)
    
    if reset:
        _add_documents(data, vectorstore)
    
    if additional_data:
        _add_documents(additional_data, vectorstore)

    qa_chain = analyzer.get_qa_chain(vectorstore)
    print("QA chain created. You can now ask questions about the documents. You can exit by typing 'exit'.")
    question = input("Enter your question: ")
    while question.lower() != 'exit':
        result = qa_chain.invoke(question)
        print("Answer: ", result['result'])
        if source:
            print("\nSources used:")
            for doc in result["source_documents"]:
                print(doc.metadata)
        question = input("Enter your question: ")