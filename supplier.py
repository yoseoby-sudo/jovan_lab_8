class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self._supplier_id: str = supplier_id
        self._name: str = name
        self._contact_email: str = contact_email

    @property
    def supplier_id(self) -> str:
        return self._supplier_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def contact_email(self) -> str:
        return self._contact_email

    def display_information(self) -> str:
        return f"Supplier ID: {self._supplier_id} | Name: {self._name} | Email: {self._contact_email}"