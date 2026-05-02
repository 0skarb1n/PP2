import csv
import json
from connect import get_connection

def get_conn():
    return get_connection()

def add_contact(name, email=None, birthday=None, group_name=None):
    conn = get_conn()
    cur = conn.cursor()
    group_id = None
    if group_name:
        cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
        row = cur.fetchone()
        if row:
            group_id = row[0]
    cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s)",
                (name, email, birthday, group_id))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Контакт '{name}' добавлен.")

def delete_contact(name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Контакт '{name}' удалён.")

def import_from_csv(filename='contacts.csv'):
    conn = get_conn()
    cur = conn.cursor()
    with open(filename, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            group_id = None
            if row.get('group'):
                cur.execute("SELECT id FROM groups WHERE name = %s", (row['group'],))
                g = cur.fetchone()
                if g:
                    group_id = g[0]
            cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id",
                        (row['name'], row.get('email') or None, row.get('birthday') or None, group_id))
            contact_id = cur.fetchone()[0]
            if row.get('phone'):
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                            (contact_id, row['phone'], row.get('type', 'mobile')))
    conn.commit()
    cur.close()
    conn.close()
    print("CSV импортирован!")

def export_to_json(filename='contacts.json'):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""SELECT c.id, c.name, c.email, c.birthday::text, g.name
                   FROM contacts c LEFT JOIN groups g ON g.id = c.group_id ORDER BY c.name""")
    result = []
    for c in cur.fetchall():
        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (c[0],))
        result.append({"name": c[1], "email": c[2], "birthday": c[3], "group": c[4],
                       "phones": [{"phone": p[0], "type": p[1]} for p in cur.fetchall()]})
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    cur.close()
    conn.close()
    print(f"Экспортировано {len(result)} контактов.")

def import_from_json(filename='contacts.json'):
    conn = get_conn()
    cur = conn.cursor()
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for contact in data:
        cur.execute("SELECT id FROM contacts WHERE name = %s", (contact['name'],))
        if cur.fetchone():
            choice = input(f"'{contact['name']}' уже есть. [s]кип / [o]верврайт? ").strip().lower()
            if choice == 'o':
                cur.execute("DELETE FROM contacts WHERE name = %s", (contact['name'],))
            else:
                continue
        group_id = None
        if contact.get('group'):
            cur.execute("SELECT id FROM groups WHERE name = %s", (contact['group'],))
            g = cur.fetchone()
            if g:
                group_id = g[0]
            else:
                cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (contact['group'],))
                group_id = cur.fetchone()[0]
        cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id",
                    (contact.get('name'), contact.get('email'), contact.get('birthday'), group_id))
        contact_id = cur.fetchone()[0]
        for p in contact.get('phones', []):
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                        (contact_id, p['phone'], p.get('type', 'mobile')))
    conn.commit()
    cur.close()
    conn.close()
    print("JSON импортирован!")

def search_contacts(query):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    if not rows:
        print("Ничего не найдено.")
    for row in rows:
        print(f"  {row[0]} | {row[1]} | {row[2]} ({row[3]}) | {row[4]}")
    cur.close()
    conn.close()

def filter_by_group(group_name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""SELECT c.name, c.email, c.birthday, g.name FROM contacts c
                   LEFT JOIN groups g ON g.id = c.group_id WHERE g.name ILIKE %s ORDER BY c.name""",
                (f"%{group_name}%",))
    rows = cur.fetchall()
    if not rows:
        print("Не найдено.")
    for row in rows:
        print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]}")
    cur.close()
    conn.close()

def search_by_email(email_query):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""SELECT c.name, c.email, g.name FROM contacts c
                   LEFT JOIN groups g ON g.id = c.group_id WHERE c.email ILIKE %s""",
                (f"%{email_query}%",))
    rows = cur.fetchall()
    if not rows:
        print("Не найдено.")
    for row in rows:
        print(f"  {row[0]} | {row[1]} | {row[2]}")
    cur.close()
    conn.close()

def show_sorted(sort_by='name'):
    order = {'name': 'c.name', 'birthday': 'c.birthday', 'date': 'c.created_at'}.get(sort_by, 'c.name')
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"""SELECT c.name, c.email, c.birthday, g.name FROM contacts c
                    LEFT JOIN groups g ON g.id = c.group_id ORDER BY {order}""")
    for row in cur.fetchall():
        print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]}")
    cur.close()
    conn.close()

def paginated_view(page_size=3):
    offset = 0
    while True:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (page_size, offset))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if not rows:
            print("Больше нет.")
            break
        print(f"\n--- {offset+1}–{offset+len(rows)} ---")
        for row in rows:
            print(f"  {row[1]} | {row[2]} | {row[3]} | {row[4]}")
        nav = input("[n]ext / [p]rev / [q]uit: ").strip().lower()
        if nav == 'n':
            offset += page_size
        elif nav == 'p':
            offset = max(0, offset - page_size)
        elif nav == 'q':
            break

def call_add_phone(name, phone, ptype):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
    conn.commit()
    cur.close()
    conn.close()
    print("Телефон добавлен.")

def call_move_to_group(name, group):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Перемещён в группу '{group}'.")

def main():
    while True:
        print("""
1. Добавить контакт     7. Пагинация
2. Удалить контакт      8. Добавить телефон
3. Поиск                9. Переместить в группу
4. Фильтр по группе    10. Импорт CSV
5. Поиск по email      11. Экспорт JSON
6. Показать/сортировка 12. Импорт JSON
0. Выход""")
        choice = input("Выбери: ").strip()
        if choice == '1':
            add_contact(input("Имя: "), input("Email: ") or None,
                        input("День рождения (YYYY-MM-DD): ") or None, input("Группа: ") or None)
        elif choice == '2':
            delete_contact(input("Имя: "))
        elif choice == '3':
            search_contacts(input("Запрос: "))
        elif choice == '4':
            filter_by_group(input("Группа: "))
        elif choice == '5':
            search_by_email(input("Email: "))
        elif choice == '6':
            show_sorted(input("Сортировка (name/birthday/date): ") or 'name')
        elif choice == '7':
            paginated_view()
        elif choice == '8':
            call_add_phone(input("Имя: "), input("Телефон: "), input("Тип (home/work/mobile): "))
        elif choice == '9':
            call_move_to_group(input("Имя: "), input("Группа: "))
        elif choice == '10':
            import_from_csv(input("CSV файл: ") or 'contacts.csv')
        elif choice == '11':
            export_to_json(input("JSON файл: ") or 'contacts.json')
        elif choice == '12':
            import_from_json(input("JSON файл: ") or 'contacts.json')
        elif choice == '0':
            break

if __name__ == "__main__":
    main()