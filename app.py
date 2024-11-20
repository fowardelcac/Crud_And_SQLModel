from databse import ENGINE, create_db_and_tables
from models import Purchase, Receipt, Product
from sqlmodel import Session, select
from decimal import Decimal
from typing import List, Union


class Create:
    def insert_product(prod_name: str):
        try:
            if prod_name == "":
                raise ValueError("Product name must not be empty")
            with Session(ENGINE) as session:
                session.add(Product(name=prod_name))
                session.commit()
        except Exception as e:
            return f"Error: {e}"

    def insert_purchase(amount: Decimal, unit_price: Decimal, product_id: int):
        try:
            if amount <= 0 or unit_price <= 0:
                raise ValueError("Amount and unit price must be greater than zero.")
            total = unit_price * amount
            with Session(ENGINE) as session:
                session.add(
                    Purchase(
                        amount=Decimal(amount),
                        unit_price=Decimal(unit_price),
                        total=Decimal(total),
                        product_id=product_id,
                    )
                )
                session.commit()

        except Exception as e:
            return f"Error: {e}"

    def insert_receipt(date: str, purchase_id: int):
        try:
            with Session(ENGINE) as session:
                session.add(Receipt(date=date, purchase_id=purchase_id))
                session.commit()
        except Exception as e:
            return f"Error: {e}"


class Read:
    def read_all(table: List[Union[Product, Purchase, Receipt]]):
        try:
            with Session(ENGINE) as session:
                query_result = session.exec(select(table)).all()
                return query_result
        except Exception as e:
            print("Error:", e)

    def read_by_id(table: List[Union[Product, Purchase, Receipt]], id: int):
        try:
            with Session(ENGINE) as session:
                query_result = session.exec(select(table).where(table.id == id)).first()
                if query_result is None:
                    return "It doesn't exist."
                return query_result
        except Exception as e:
            print("Error:", e)

    def read_by_feature(
        table: List[Union[Product, Purchase, Receipt]], feature_name, feature_value
    ):
        try:
            with Session(ENGINE) as session:
                query_result = session.exec(
                    select(table).where(feature_name == feature_value)
                ).first()
                if query_result is None:
                    return "It doesn't exist."
                return query_result
        except Exception as e:
            print("Error:", e)


class Update:
    def update_product(prod_id: int, new_name: str):

        try:
            if prod_id <= 0:
                raise ValueError("The ID can't be equal/lower than zero.")
            if new_name == "":
                raise ValueError("Product name must not be empty.")
            with Session(ENGINE) as session:
                query = select(Product).where(Product.id == prod_id)
                result = session.exec(query).one()
                result.name = new_name
                session.add(result)
                session.commit()
        except Exception as e:
            return f"Error: {e}"

    def update_purchase(
        prod_id: int,
        new_amount: Decimal = None,
        new_unit: Decimal = None,
        new_product_id: int = None,
    ):
        if (prod_id or new_product_id) <= 0:
            raise ValueError("The ID can't be equal/lower than zero.")
        try:
            with Session(ENGINE) as session:
                query = select(Purchase).where(Purchase.id == prod_id)
                result = session.exec(query).one()

                if new_amount is not None and new_amount > 0:
                    result.amount = new_amount
                if new_unit is not None and new_unit > 0:
                    result.unit_price = new_unit
                if Read.read_by_id(Product, new_product_id) is not None:
                    result.product_id = new_product_id

                session.add(result)
                session.commit()

                session.refresh(result)
                result.total = result.amount * result.unit_price
                session.add(result)
                session.commit()
        except Exception as e:
            return f"Error: {e}"

    def update_receipt(
        receipt_id: int, new_date: str = None, new_purchase_id: int = None
    ):
        if receipt_id <= 0:
            raise ValueError("The ID can't be equal/lower than zero.")
        try:
            with Session(ENGINE) as session:
                query = select(Receipt).where(Receipt.id == receipt_id)
                result = session.exec(query).one()
                if new_date is not None:
                    result.date = new_date
                if Read.read_by_id(Purchase, new_purchase_id) is not None:
                    result.purchase_id = new_purchase_id

                session.add(result)
                session.commit()
        except Exception as e:
            return f"Error: {e}"


class Delete:
    def delete(table: List[Union[Product, Purchase, Receipt]], feature_name, feature):
        try:
            with Session(ENGINE) as session:
                query = select(table).where(feature_name == feature)
                result = session.exec(query).one()
                session.delete(result)
                session.commit()
        except Exception as e:
            return f"Error: {e}"


def build_products():
    prod_name = [
        "Vainilla",
        "Chocolate",
        "Fresa",
        "Menta",
        "Stracciatella",
        "Café",
        "Coco",
        "Nuez",
        "Frambuesa",
        "Pistacho",
    ]
    with Session(ENGINE) as session:
        products = [Product(name=name) for name in prod_name]
        session.add_all(products)
        session.commit()


def main():
    create_db_and_tables()
    build_products()


if __name__ == "__main__":
    main()
