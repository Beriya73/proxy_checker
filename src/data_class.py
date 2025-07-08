from dataclasses import dataclass


@dataclass
class ProxyResult:
    working: bool
    ip: str = ""
    country: str = ""
    region: str = ""
    city: str = ""
    isp: str = ""
    resptime: float = 0
    proxy: str=""
    error: str = ""

    def __str__(self) -> str:
        if self.working:
            parts = [
                f"IP: {self.ip}",
                f"Location: {self.country}, {self.city}",
                f"ISP: {self.isp}",
                f"Delay: {self.resptime:.2f}s"
            ]
            return " | ".join(parts)
        else:
            return f"FAILED | Error: {self.error}"

