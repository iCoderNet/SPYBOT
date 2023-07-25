# SPYBOT
Foydalanuvchini bot orqali kuzatish uchun maxsus

### O'rnatish
GitHubdan yuklab oling
```sh
git clone https://github.com/iCoderNet/SPYBOT
```

Virtual muhit yarating
```sh
python -m venv env
```

Virtual muhitni faollashtiring
```sh
env\Scripts\activate
```

Kerakli kutubxonalarni o'rnating
```sh
pip install -r requirments.txt
```

### O'zgartirish
Telegramda yangi bot yarating va yaratgan botingiz tokenini nusxalang
`main.py` faylida `BOT_TOKEN` o'zgaruvchisi mavjud nusxalagan botingiz tokenini joylang.
`main.py` faylidagi `ADMIN_ID` o'zgaruvchisiga o'zingizni ID raqamingizni kiriting


### Ishga tushirish
python orqali run qilasiz
```sh
python main.py
```

### EXE ga o'tkazish

```sh
pyinstaller --onefile --noconsole main.py
```
