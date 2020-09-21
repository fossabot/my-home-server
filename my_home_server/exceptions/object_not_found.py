from typing import Optional


class ObjectNotFoundException(Exception):
    def __init__(self, entity_name: str, entity_identifier: Optional[dict]):
        super().__init__(f"{entity_name} not found. {'Identifier: {str(entity_identifier)}' if entity_identifier else 'No identifier'}")