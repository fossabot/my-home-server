from typing import List, Optional

from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.product_mapper import ProductMapper
from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.models.purchase_list_product import PurchaseListProduct
from my_home_server.models.purchase_list import PurchaseList


class PurchaseListMapper(MapperInterface):
    def __init__(self):
        self.user_mapper = UserMapper()
        self.product_mapper = ProductMapper()

    def to_dto(self, obj: PurchaseList) -> Optional[dict]:
        if not obj:
            return None

        return {
            "id": obj.id,
            "name": obj.name,
            "created_at": obj.created_at,
            "created_by": self.user_mapper.to_dto(obj.created_by),
            "purchase_products": self.__products_to_dto(obj.purchase_products)
        }

    def to_object(self, dto: dict, loaded_object: PurchaseList = None) -> Optional[PurchaseList]:
        if not dto:
            return None

        purchase_list = loaded_object if loaded_object else PurchaseList()
        purchase_list.id = dto.get("id")
        purchase_list.name = dto.get("name")
        purchase_list.purchase_products = self.__products_to_obj(dto.get("purchase_products"))

        if not loaded_object:
            purchase_list.created_by = self.user_mapper.to_object(dto.get("created_by"))
            purchase_list.created_at = dto.get("created_at")

        return purchase_list

    def validate_dto(self, dto: dict):
        self.generic_validate_dto(dto, ["name", "purchase_products"], PurchaseList.__name__)

    def __products_to_obj(self, purchase_products_dto: List[dict]) -> List[PurchaseListProduct]:
        products = list()
        for dto in purchase_products_dto:
            purchase_product = PurchaseListProduct()
            purchase_product.product = self.product_mapper.to_object(dto)
            purchase_product.quantity = dto.get("quantity")
            purchase_product.value = dto.get("value")
            products.append(purchase_product)

        return products

    def __products_to_dto(self, purchase_products: List[PurchaseListProduct]) -> List[dict]:
        products = list()
        for purchase_product in purchase_products:
            dto = self.product_mapper.to_dto(purchase_product.product)

            dto.update({
                "value": purchase_product.value,
                "quantity": purchase_product.quantity
            })

            products.append(dto)

        return products
