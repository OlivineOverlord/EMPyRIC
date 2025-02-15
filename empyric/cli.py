import argparse
import pandas as pd
from empyric.storage import HDF5Storage

def main():
    parser = argparse.ArgumentParser(description="EMPyRIC: Geochemical Data Storage System")
    parser.add_argument("action", choices=["save", "load", "query"], help="Action to perform")
    parser.add_argument("--file", type=str, default="geochem_data.h5", help="HDF5 file name")
    parser.add_argument("--group", type=str, required=True, help="HDF5 group (e.g., 'geochem')")
    parser.add_argument("--dataset", type=str, required=True, help="HDF5 dataset (e.g., 'samples')")
    parser.add_argument("--csv", type=str, help="CSV file to save/load data")
    parser.add_argument("--query", type=str, help="Query string (e.g., 'SiO2 > 50')")

    args = parser.parse_args()
    storage = HDF5Storage(args.file)

    if args.action == "save":
        if not args.csv:
            print("Error: --csv is required to save data.")
            return
        df = pd.read_csv(args.csv)
        storage.save_dataframe(df, args.group, args.dataset)
        print(f"Data saved to {args.file} under {args.group}/{args.dataset}")

    elif args.action == "load":
        df = storage.load_dataframe(args.group, args.dataset)
        print(df)

    elif args.action == "query":
        if not args.query:
            print("Error: --query is required for querying.")
            return
        df = storage.query(args.group, args.dataset, args.query)
        print(df)

if __name__ == "__main__":
    main()