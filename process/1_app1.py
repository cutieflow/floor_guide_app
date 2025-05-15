floors = {
    "1F": {
        "name": "1階",
        "services": ["市民税課", "資産税課", "収納課", "市民課", "国保年金課", 
                     "生活環境課", "消費生活センター", "福祉課", "長寿社会課",
                     "水道課", "会計課"],
    },
    "2F": {
        "name": "2階",
        "services": ["財政課"],
    },
    "3F": {
        "name": "3階",
        "services": ["総務課", "政策企画課", "ILC推進課",
                     "プロジェクト推進室", "女性活躍推進室", "若者活躍推進室"
                     "広聴広報課", "秘書課", "職員課"],
    },
    "4F": {
        "name": "4階",
        "services": ["農政推進課", "生産流通課", "林政推進課", "治水河川課",
                     "都市整備課", "道路建設課", "道路管理課"],
    },
    "5F": {
        "name": "5階",
        "services": ["総務課", "下水道課", "留守家庭児童クラブ推進課", 
                     "商政・労政課", "観光物産課", "工業振興課", "起業支援室"],
    }
}

def show_menu():
    print("\n🏢 市役所庁舎 フロアガイド")
    print("以下の階を選んでください（例：1F）")
    for key in floors:
        print(f"- {key} ({floors[key]['name']})")
    print("- exit（終了）")


def show_floor_info(floor_key):
    floor = floors.get(floor_key.upper())
    if floor:
        print(f"\n📍 {floor['name']} にある課・サービス：")
        for service in floor['services']:
            print(f"  - {service}")
    else:
        print("⚠️ その階は存在しません。")


def main():
    while True:
        show_menu()
        choice = input(">> 選択: ").strip()
        if choice.lower() == "exit":
            print("ご利用ありがとうございました。")
            break
        show_floor_info(choice)


if __name__ == "__main__":
    main()
