from databse import ENGINE
from models import *
from sqlmodel import select, Session
from app import Create, Update, Read, Delete, main
import pytest


def test_create_read():
    main()
    query1 = Read.read_by_id(Product, 1)
    assert query1.name == "Vainilla"

    assert Create.insert_product("") == "Error: Product name must not be empty"

    Create.insert_product("Banana")
    assert Read.read_by_feature(Product, Product.name, "Banana") is not None

    error = Create.insert_purchase(0, 0, 100)
    assert error == "Error: Amount and unit price must be greater than zero."

    Create.insert_purchase(1, 10, 1)
    queri = Read.read_by_id(Purchase, 1)
    assert queri.total == round(Decimal(10), 2)

    Create.insert_receipt("2010/10/01", 1)
    Create.insert_receipt("The param accepts str so...", 1)
    query = Read.read_by_id(Receipt, 2)
    assert query.date == "The param accepts str so..."

    all_prods = Read.read_all(Product)
    n = len(all_prods)

    assert n == 11


def test_update():
    assert (
        Update.update_product(0, "") == "Error: The ID can't be equal/lower than zero."
    )

    Create.insert_product("Bad name")
    Update.update_product(12, "Manzana")

    query = Read.read_by_id(Product, 12)
    assert query.name == "Manzana"

    Update.update_purchase(1, 5.66, 10)
    query_purch = Read.read_by_id(Purchase, 1)
    assert query_purch.total == round(Decimal(5.66 * 10), 2)

    Update.update_receipt(2, "2024/10/11")
    query = Read.read_by_id(Receipt, 2)
    assert query.date != "The param accepts str so..."


def test_delete():
    Delete.delete(Receipt, Receipt.id, 2)
    Delete.delete(Receipt, Receipt.id, 1)

    assert Read.read_all(Receipt) == []

    Delete.delete(Product, Product.name, "Stracciatella")
    query = Read.read_by_feature(Product, Product.name, "Stracciatella")
    assert query == "It doesn't exist."
