import argparse
import asyncio
import csv
import sys
import json

from graffiti_lookup.main import GraffitiLookup


SUPPORTED_FILE_TYPES = ("csv", "json")

parser = argparse.ArgumentParser()

parser = argparse.ArgumentParser(description="Fetch NYC Graffiti Service Request")
parser.add_argument(
    "-i",
    "--id",
    help="graffiti service request id",
)
parser.add_argument(
    "-L", "--ids", help="Comma separated list of graffiti service request ids"
)
parser.add_argument(
    "-f",
    "--file-path",
    help="The output file path for the requested graffiti service request records",
)
parser.add_argument(
    "-m",
    "--merge-file",
    action="store_true",
    help="Merge graffiti request records with existing file",
)
parser.add_argument(
    "-t", "--file-type", choices=SUPPORTED_FILE_TYPES, help="The output file type"
)

args = parser.parse_args()


def read_file(file_path, file_type, result, fieldnames):
    with open(file_path, "r") as file:
        if file_type == "json":
            return json.loads(file.read())
        elif file_type == "csv":
            csv_reader = csv.DictReader(file, fieldnames=fieldnames)
            return [row for row in csv_reader][1:]
        else:
            sys.stderr.write(
                f"Unsupported file-type {file_type} not in {SUPPORTED_FILE_TYPES}"
            )


def write_file(file_path, file_type, result, fieldnames):
    with open(file_path, "w") as file:
        if file_type == "json":
            file.write(json.dumps(result, indent=4))
        elif file_type == "csv":
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            if args.ids:
                csv_writer.writerows(result)
            else:
                csv_writer.writerow(result)
        else:
            sys.stderr.write(
                f"Unsupported file-type {file_type} not in {SUPPORTED_FILE_TYPES}"
            )


async def main():
    graffiti_lookup_service = GraffitiLookup()
    result = None
    file_path = args.file_path
    file_type = args.file_type or (file_path and file_path.split(".")[-1].lower())

    if args.id:
        result = await graffiti_lookup_service.get_status_by_id(args.id)

    if args.ids:
        service_ids = args.ids.replace(" ", "").split(",")
        result = await graffiti_lookup_service.get_statuses_by_id(service_ids)

    try:
        fieldnames = result[0].keys() if args.ids else result.keys()
    except (IndexError, AttributeError):
        fieldnames = []

    if not file_path:
        sys.stdout.write(json.dumps(result))
    else:
        if args.merge_file:
            file_results = read_file(file_path, file_type, result, fieldnames)
            file_result_map = {
                row.get(GraffitiLookup.ID_FIELD): row for row in file_results
            }
            result_map = {row.get(GraffitiLookup.ID_FIELD): row for row in result}
            all_results = {**file_result_map, **result_map}
            result = list(all_results.values())

        write_file(file_path, file_type, result, fieldnames)


if __name__ == "__main__":
    asyncio.run(main())
