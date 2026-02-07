from db import add_reklamacja, list_reklamacje


def main():
    print("=== LISTA ZGŁOSZEŃ ===\n")

    reklamacje = list_reklamacje()

    if not reklamacje:
        print("Brak zgłoszeń w bazie.")
        return

    for r in reklamacje:
        print(f"ID: {r[0]}")
        print(f"Data: {r[1]}")
        print(f"Tytuł: {r[2]}")
        print(f"Ilość: {r[3]}")
        print(f"Status: {r[4]}")
        print(f"Zgłaszający: {r[5]}")
        print(f"Nr zgłoszenia: {r[6]}")
        print("-" * 30)


if __name__ == "__main__":
    main()
