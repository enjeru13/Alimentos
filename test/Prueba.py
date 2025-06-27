# genera_alimentos_seed.py

import random
import datetime

# Nombre de tu tabla y columnas (sin id_producto, que es AUTO_INCREMENT)
TABLE = "alimentos"
COLUMNS = (
    "id_categoria",
    "nom_producto",
    "calorias",
    "proteina",
    "grasas",
    "carbohidratos",
    "descripcion",
    "imagen_url",
    "fecha_registro",
)

# Número de categorías que ya tienes en tu DB
NUM_CATS = 10

# Para componer nombres
ADJECTIVES = [
    "Fresco",
    "Natural",
    "Orgánico",
    "Dulce",
    "Crujiente",
    "Exótico",
    "Tostado",
    "Marinado",
    "Congelado",
    "Delicioso",
]
NOUNS = [
    "Manzana",
    "Banana",
    "Zanahoria",
    "Leche",
    "Carne",
    "Pan",
    "Arroz",
    "Jugo",
    "Frijol",
    "Nuez",
    "Queso",
    "Pescado",
    "Huevo",
]


def make_description(name, cat_id):
    return f"{name} (categoría #{cat_id}) de alta calidad."


def fmt(value):
    return str(round(value, 2))


def main():
    with open("alimentos_seed.sql", "w", encoding="utf-8") as f:
        for i in range(1, 1001):
            # el id_categoria será un entero aleatorio 1..NUM_CATS
            cat_id = random.randint(1, NUM_CATS)
            adj = random.choice(ADJECTIVES)
            noun = random.choice(NOUNS)
            name = f"{adj} {noun} {i}"
            cal = random.uniform(5, 600)
            pro = random.uniform(0, 50)
            gra = random.uniform(0, 50)
            carb = random.uniform(0, 100)
            desc = make_description(name, cat_id)
            img = f"media/images/{noun.lower()}{i%20}.jpg"
            fecha = datetime.datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")

            safe_name = name.replace("'", "''")
            safe_desc = desc.replace("'", "''")

            vals = (
                str(cat_id),
                f"'{safe_name}'",
                fmt(cal),
                fmt(pro),
                fmt(gra),
                fmt(carb),
                f"'{safe_desc}'",
                f"'{img}'",
                fecha,
            )
            line = (
                f"INSERT INTO {TABLE} "
                f"({', '.join(COLUMNS)}) VALUES ({', '.join(vals)});\n"
            )
            f.write(line)
    print("✅ Semilla creada en `alimentos_seed.sql`")


if __name__ == "__main__":
    main()
