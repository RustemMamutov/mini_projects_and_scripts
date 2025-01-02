from enum import Enum
from dataclasses import dataclass
from pathlib import Path
import csv

BASE_DIR = str(Path().resolve())

SOURCE_DATA_DIR = "SOURCE_DATA_DIR"
FILENAME_PATTERN = "FILENAME_PATTERN"


@dataclass(unsafe_hash=True)
class Spend:
    month: int
    description: str
    code: str
    amount: int


class SpendType(Enum):
    Income = "Income",
    Outcome = "Outcome"


class Person(Enum):
    One = "One"
    Two = "Two"


@dataclass(unsafe_hash=True)
class Category:
    code: str
    description: str


CATEGORIES_FILENAME = {
    Person.One:  "Person1_categories.csv",
    Person.Two: "Person2_categories.csv"
}

CATEGORIES_START_SYMBOL = {
    SpendType.Income: "Д",
    SpendType.Outcome: "Р"
}


def read_categories_from_file(person: Person, spend_type: SpendType):
    list_of_categories = list()
    with open("{}/{}".format(BASE_DIR, CATEGORIES_FILENAME[person]), newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if CATEGORIES_START_SYMBOL[spend_type] in row[0]:
                list_of_categories.append(Category(row[0], row[1]))

    return list_of_categories


CATEGORIES = {
    SpendType.Income: {
        Person.One: read_categories_from_file(Person.One, SpendType.Income),
        Person.Two: read_categories_from_file(Person.Two, SpendType.Income),
    },
    SpendType.Outcome: {
        Person.One: read_categories_from_file(Person.One, SpendType.Outcome),
        Person.Two: read_categories_from_file(Person.Two, SpendType.Outcome)
    }
}


def prepare_category_codes(person: Person):
    return {
        SpendType.Income: [category.code for category in CATEGORIES[SpendType.Income][person]],
        SpendType.Outcome: [category.code for category in CATEGORIES[SpendType.Outcome][person]],
    }


def prepare_category_desc_by_code_dict(person: Person):
    result = dict()
    for inc in CATEGORIES[SpendType.Income][person]:
        result[inc.code] = inc.description
    for out in CATEGORIES[SpendType.Outcome][person]:
        result[out.code] = out.description
    return result


sheets = {
    Person.One: ["{}".format(x) for x in range(1, 13)],
    Person.Two: ["{}А".format(x) for x in range(1, 13)]
}
