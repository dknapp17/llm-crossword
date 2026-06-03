import sys
import traceback
from datetime import datetime, timedelta

from llm_cw.domain.documents import CrosswordDocument
from llm_cw.ingestion.ingestion import ingest_crossword


def parse_date(arg: str) -> datetime:
    return datetime.strptime(arg, "%Y-%m-%d")


def iter_dates(start: datetime, end: datetime):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def main():
    try:
        if len(sys.argv) < 3:
            raise ValueError(
                "Usage: python ingest_crossword.py YYYY-MM-DD YYYY-MM-DD"
            )

        start_date = parse_date(sys.argv[1])
        end_date = parse_date(sys.argv[2])

        total_docs = 0

        for puzzle_date in iter_dates(start_date, end_date):
            print(f"\nIngesting {puzzle_date.date()}...")

            try:
                docs = ingest_crossword(puzzle_date)

                if not docs:
                    print(f"No documents generated for {puzzle_date.date()}")
                    continue

                CrosswordDocument.bulk_insert(docs)

                print(f"Inserted {len(docs)} documents")
                total_docs += len(docs)

            except Exception as e:
                print(f"\n❌ Failed ingestion for {puzzle_date.date()}")
                print(f"Error: {repr(e)}")
                traceback.print_exc()
                continue

        print(f"\nDone. Total inserted: {total_docs}")

    except Exception as e:
        print(f"Failed ingestion run: {e}")
        raise


if __name__ == "__main__":
    main()