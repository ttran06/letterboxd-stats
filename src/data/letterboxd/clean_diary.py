import argparse
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="remove old diary entries")

    parser.add_argument("new_diary", help="New letterboxd diary")
    parser.add_argument(
        "--old_diary", default="old_diary.csv", help="Old letterboxd diary"
    )
    parser.add_argument(
        "--output", default=".", help="Output path of cleaned diary file"
    )

    return parser.parse_args()


def clean_diary(new_diary: str, old_diary: str):
    new_diary = pd.read_csv(new_diary)
    old_diary = pd.read_csv(old_diary)
    old_diary.drop(columns=["Name", "Tags", "Watched Date"], inplace=True)

    joined_diary = pd.merge(
        new_diary,
        old_diary,
        how="outer",
        on=["Date", "Year", "Letterboxd URI", "Rating", "Rewatch"],
        indicator=True,
    )

    left_only = joined_diary.loc[joined_diary["_merge"] == "left_only"]
    print(joined_diary[joined_diary["Name"] == "Portrait of a Lady on Fire"])

    # left_only.to_csv("cleaned_diary.csv")


def main():
    args = parse_args()

    clean_diary(args.new_diary, args.old_diary)


if __name__ == "__main__":
    main()
