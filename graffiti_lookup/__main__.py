import argparse
import sys
import json

from graffiti_lookup.main import GraffitiLookup

parser = argparse.ArgumentParser()

parser = argparse.ArgumentParser(
    description="Fetch NYC Graffiti Service Request"
)
parser.add_argument(
    "-i",
    "--id",
    help="graffiti service request id",
)
parser.add_argument(
    "-L",
    "--ids",
    help="Comma separated list of graffiti service request ids"
)

args = parser.parse_args()


if __name__ == "__main__":
    graffiti_lookup_service = GraffitiLookup()

    if args.id:
        record = graffiti_lookup_service.get_status_by_id(args.id)
        sys.stdout.write(f"{json.dumps(record)}")

    if args.ids:
        service_ids = args.ids.split(",")
        records = graffiti_lookup_service.get_statuses_by_id(service_ids)
        sys.stdout.write(f"{json.dumps(records)}")
