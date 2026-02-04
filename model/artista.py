from dataclasses import dataclass
@dataclass
class Artista:
    artist_id: int
    name: str

    def __repr__(self):
        return f"{self.name} -->"

    def __hash__(self):
        return hash(self.artist_id)