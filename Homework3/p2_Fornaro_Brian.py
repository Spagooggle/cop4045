# -*- coding: utf-8 -*-
class ParkingPermit:
    """Store the owner's name, permit duration, and fee schedule."""

    def __init__(self, owner: str, months: int, fees: dict[str, float]) -> None:
        """Create a permit; months must be at least 1."""
        if months < 1:
            raise ValueError("Months must be at least 1")
        self.owner = owner
        self.months = months
        self.fees = fees.copy()

    def cost(self) -> float:
        """Return the permit cost, as calculated by a subclass."""
        raise NotImplementedError("Cost must be defined by a subclass")

    def __str__(self) -> str:
        """Return a readable description of the permit."""
        return f"Parking permit for {self.owner}, {self.months} months"

    def __repr__(self) -> str:
        """Return a detailed representation of the permit."""
        return f"ParkingPermit({self.owner!r}, {self.months!r}, {self.fees!r})"


class StudentPermit(ParkingPermit):
    """A student parking permit that also tracks registered vehicles."""

    def __init__(self, owner: str, months: int,
                 fees: dict[str, float], vehicles: int) -> None:
        """Create a student permit; vehicles must be at least 1."""
        super().__init__(owner, months, fees)
        if vehicles < 1:
            raise ValueError("Vehicles must be at least 1")
        self.vehicles = vehicles

    def cost(self) -> float:
        """Return the monthly fee plus fees for extra vehicles."""
        return (self.months * self.fees["student_monthly"] +
                (self.vehicles - 1) * self.fees["extra_vehicle"])

    def __str__(self) -> str:
        """Return the student's name and total permit cost."""
        return f"Student: {self.owner} - ${self.cost():.2f}"

    def __repr__(self) -> str:
        """Return a detailed representation of the student permit."""
        return (f"StudentPermit({self.owner!r}, {self.months!r}, "
                f"{self.fees!r}, {self.vehicles!r})")


class FacultyPermit(ParkingPermit):
    """A faculty parking permit with optional garage access."""

    def __init__(self, owner: str, months: int,
                 fees: dict[str, float], garage: bool) -> None:
        """Create a faculty permit and set garage access."""
        super().__init__(owner, months, fees)
        self.garage = garage

    def cost(self) -> float:
        """Return the monthly fee plus garage fees when included."""
        total = self.months * self.fees["faculty_monthly"]
        if self.garage:
            total += self.months * self.fees["garage_monthly"]
        return total

    def __str__(self) -> str:
        """Return the faculty member's name and total permit cost."""
        return f"Faculty: {self.owner} - ${self.cost():.2f}"

    def __repr__(self) -> str:
        """Return a detailed representation of the faculty permit."""
        return (f"FacultyPermit({self.owner!r}, {self.months!r}, "
                f"{self.fees!r}, {self.garage!r})")


def summarize_list(permits: list[ParkingPermit]) -> float:
    """Print each permit owner's name and cost, then return total revenue."""
    total = 0.0
    for permit in permits:
        print(permit)
        total += permit.cost()
    return total


def main() -> None:
    """Create student and faculty permits and show their costs."""
    print("Z23672108")
    print("Problem 2 - Parking Permits\n")

    fees = {
        "student_monthly": 25.0,
        "extra_vehicle": 10.0,
        "faculty_monthly": 40.0,
        "garage_monthly": 15.0
    }

    permits = [
        StudentPermit("Alex Johnson", 4, fees, 2),
        StudentPermit("Sam Carter", 2, fees, 1),
        FacultyPermit("Dr. Smith", 3, fees, True),
        FacultyPermit("Dr. Taylor", 2, fees, False)
    ]

    print("Permit objects:")
    for permit in permits:
        print(repr(permit))

    print("\nPermit costs:")
    revenue = summarize_list(permits)
    print(f"\nTotal revenue: ${revenue:.2f}")


if __name__ == "__main__":
    main()

