import urllib.request
import json
import time

def post_data(url, data):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except Exception as e:
        return 0, str(e)


def seed_stock():
    print("Seeding Stock...")
    url = "http://localhost:8001/stocks/"
    items = [
        {"name": "Carton ondulé A4", "category": "raw_material", "quantity": 5000, "unit": "kg", "min_threshold": 1000},
        {"name": "Encre noire industrielle", "category": "consumable", "quantity": 150, "unit": "litres", "min_threshold": 50},
        {"name": "Boîte Standard 30x30", "category": "finished_product", "quantity": 2500, "unit": "unités", "min_threshold": 500},
        {"name": "Colle industrielle", "category": "consumable", "quantity": 80, "unit": "kg", "min_threshold": 20},
    ]
    for item in items:
        status, resp = post_data(url, item)
        if status == 201:
            print(f"  [OK] Added stock: {item['name']}")
        else:
            print(f"  [FAIL] Failed to add stock {item['name']}: {resp}")


def seed_machines():
    print("Seeding Machines...")
    url = "http://localhost:8004/machines/"
    machines = [
        {"name": "Découpeuse Laser Alpha", "machine_type": "découpeuse", "location": "Atelier A", "capacity_per_hour": 1500, "status": "running", "serial_number": "SN-DEC-001"},
        {"name": "Plieuse Automatique Beta", "machine_type": "plieuse", "location": "Atelier B", "capacity_per_hour": 3000, "status": "stopped", "serial_number": "SN-PLI-002"},
        {"name": "Imprimeuse Couleur Gamma", "machine_type": "imprimeuse", "location": "Atelier A", "capacity_per_hour": 1000, "status": "running", "serial_number": "SN-IMP-003"},
        {"name": "Colleuse Rapide Delta", "machine_type": "colleuse", "location": "Atelier C", "capacity_per_hour": 2000, "status": "maintenance", "serial_number": "SN-COL-004"},
        {"name": "Machine BOBST L1", "machine_type": "découpeuse", "location": "Atelier Principal", "capacity_per_hour": 5000, "status": "running", "serial_number": "SN-BOBST-L1"},
    ]
    for machine in machines:
        status, resp = post_data(url, machine)
        if status == 201:
            print(f"  [OK] Added machine: {machine['name']}")
        else:
            print(f"  [FAIL] Failed to add machine {machine['name']}: {resp}")


def seed_orders():
    print("Seeding Orders...")
    url = "http://localhost:8003/orders/"
    orders = [
        {"customer_name": "Amazon", "product_name": "Boîte Standard 30x30", "quantity": 10000, "status": "confirmed", "priority": 1},
        {"customer_name": "Cdiscount", "product_name": "Carton Renforcé 50x50", "quantity": 5000, "status": "in_production", "priority": 2},
        {"customer_name": "Fnac", "product_name": "Emballage Livre M", "quantity": 2000, "status": "pending", "priority": 3},
        {"customer_name": "Boulanger", "product_name": "Boîte Électroménager L", "quantity": 500, "status": "delivered", "priority": 2},
    ]
    order_ids = []
    for order in orders:
        status, resp = post_data(url, order)
        if status == 201:
            order_ids.append(resp["id"])
            print(f"  [OK] Added order for: {order['customer_name']} (ID: {resp['id']})")
        else:
            print(f"  [FAIL] Failed to add order for {order['customer_name']}: {resp}")
    return order_ids


def seed_production(order_ids):
    print("Seeding Production...")
    url = "http://localhost:8002/productions/"
    
    if not order_ids:
        print("  [WARN] No orders to link production to.")
        return

    productions = [
        {"order_id": order_ids[1], "product_name": "Carton Renforcé 50x50", "quantity_planned": 5000, "status": "in_progress"},
        {"order_id": order_ids[2], "product_name": "Emballage Livre M", "quantity_planned": 2000, "status": "pending"},
        {"order_id": order_ids[3], "product_name": "Boîte Électroménager L", "quantity_planned": 500, "status": "completed"},
    ]
    for prod in productions:
        status, resp = post_data(url, prod)
        if status == 201:
            print(f"  [OK] Added production for order: {prod['order_id']}")
        else:
            print(f"  [FAIL] Failed to add production: {resp}")


if __name__ == "__main__":
    print("[START] Starting Data Seeding...")
    seed_stock()
    seed_machines()
    order_ids = seed_orders()
    seed_production(order_ids)
    print("[DONE] Seeding Complete!")
