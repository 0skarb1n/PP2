import json

with open("sample_data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print("DN".ljust(50), "Description".ljust(20), "Speed".ljust(8), "MTU")
print("-" * 80)

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]

    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")

    print(dn.ljust(50), descr.ljust(20), speed.ljust(8), mtu)