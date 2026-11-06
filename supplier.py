class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        if not isinstance(supplier_id, str) or not supplier_id.strip():
            raise ValueError("Supplier ID cannot be empty.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Supplier name cannot be empty.")

        if not isinstance(contact_email, str) or "@" not in contact_email:
            raise ValueError("Please provide a valid supplier email.")

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
    
    def to_dict(self) -> dict:
        return {
            "supplier_id": self._supplier_id,
            "name": self._name,
            "contact_email": self._contact_email
        }