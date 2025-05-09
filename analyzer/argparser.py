import argparse
import os

parser = argparse.ArgumentParser(description="GCAM Anamoly detector!")

parser.add_argument(
    "-d",
    "--data",
    type=str,
    nargs='+',
    default="data",
    help="Paths to the data directories containing the data files (only csvs, xlxs, pdfs, docx can be parsed). " \
    "One or more paths can be provided. Default is 'data' in the current directory.",
)

parser.add_argument(
    "-c",
    "--chunks",
    type=int,
    default=2000,
    help="Number of tokens to partition the data into. Default is 2000. Each chunk will provide local context.",
)

parser.add_argument(
    "-o",
    "--chunk_overlap",
    type=int,
    default=100,
    help="Number of tokens to overlap between chunks. Default is 100. This helps in maintaining context between chunks.",
)

parser.add_argument(
    "-n",
    "--num_chunks",
    type=int,
    default=10,
    help="Number of chunks to use for the analysis. Default is 10. This helps in limiting the number of chunks to process.",
)

parser.add_argument(
    "--text-model",
    type=str,
    default="text-embedding-3-small-birthright",
    help="The text embedding model to use for the analysis. Default is 'text-embedding-3-small-birthright'.",
)

parser.add_argument(
    "-m",
    "--model",
    type=str,
    default="gpt-4o-birthright",
    help="The model to use for the analysis. Default is 'gpt-4o-birthright'.",
)

parser.add_argument(
    "-u",
    "--base-url",
    type=str,
    default="https://ai-incubator-api.pnnl.gov",
    help="The API URL to use for the analysis. Default is 'https://ai-incubator-api.pnnl.gov'.",
)

parser.add_argument(
    "-k",
    "--api-key",
    type=str,
    default=os.getenv("AI_API_KEY"),
    metavar="AI_API_KEY",
    help="The API key to use for the analysis. Default is environment variable AI_API_KEY.",
)

parser.add_argument(
    "-p",
    "--persist-directory",
    type=str,
    default="chroma_db",
    help="The directory to persist the data. Default is 'chroma_db' in the current directory.",
)

parser.add_argument(
    "-t",
    "--temperature",
    type=float,
    default=0.0,
    help="The temperature to use for the analysis. Default is 0.0. Higher values make the output more random.",
)

parser.add_argument(
    "-r",
    "--reset",
    action="store_true",
    help="Reset the vectorstore. This will delete the existing vectorstore directory and create a new one.",
)

parser.add_argument(
    "-s",
    "--include-sources",
    action="store_true",
    help="Include sources in the output. This will include the source of the data in the output.",
)

parser.add_argument(
    "-a",
    "--add-data",
    type=str,
    nargs='+',
    default=None,
    help="Add files in a data directory to the existing vectorstore. " \
    "This will add the files to the existing vectorstore database.",
)




