# Mini ORM – Usage & Examples (Like Real Documentation)

---

# 🔌 1. Setup Database

```python
from pyframeuz.orm import Database

db = Database("./test.db")
```

---

# 🧱 2. Define Tables (Models)

```python
from pyframeuz.orm import Table, Column, ForeignKey

class Author(Table):
    name = Column(str)
    age = Column(int)


class Book(Table):
    title = Column(str)
    published = Column(bool)
    author = ForeignKey(Author)
```

---

# 🏗️ 3. Create Tables in Database

```python
db.create(Author)
db.create(Book)
```

---

# 📦 4. Create Instance (Object)

```python
author = Author(name="Ali", age=20)
```

---

# 💾 5. Save (INSERT)

```python
author.save()
```

### SQL Generated
```
INSERT INTO author (name, age) VALUES (?, ?)
```

### Params
```
("Ali", 20)
```

---

# 📖 6. Read All Data

```python
authors = Author.all()
```

### SQL
```
SELECT * FROM author
```

### Result (Mock)
```python
[
    Author(name="Ali", age=20),
    Author(name="Vali", age=25)
]
```

---

# 🔍 7. Filter Data

```python
authors = Author.filter(name="Ali")
```

### SQL
```
SELECT * FROM author WHERE name = ?
```

### Params
```
("Ali",)
```

---

# ✏️ 8. Update Data

```python
author.age = 21
author.update()
```

### SQL
```
UPDATE author SET age = ? WHERE name = ?
```

---

# ❌ 9. Delete Data

```python
author.delete()
```

### SQL
```
DELETE FROM author WHERE name = ?
```

---

# 🔄 Internal Flow

Every operation works like this:

```
Model Method → Build SQL → Database.execute() → SQLite → Result → Model Objects
```

---

# 🧠 Key Idea

- Tables are Python classes
- Rows are Python objects
- ORM converts everything into SQL automatically

---

# 🚀 Summary

Your ORM supports:

- Table creation
- Instance creation
- Insert (save)
- Select (all, filter)
- Update
- Delete

All using clean Python code without writing raw SQL.

