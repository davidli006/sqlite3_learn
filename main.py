"""
@DATE: 2022/5/3
@Author  : ld
"""
from db_model import Province, City, County, Town, Village, engine
import pandas as pd


def main():
    df = pd.read_sql("select * from `area_code_2022`;", con=engine)
    print(df)
    model_list = [Province, City, County, Town, Village]
    area_list = []
    for k, Area in enumerate(model_list):
        df_ = df[df.level == k + 1]
        for p in df_.to_dict("records"):
            area = Area(
                name=p.get("name"),
                parent_code=p.get("pcode"),
                ad_code=p.get("code"),
                card_code=str(p.get("code"))[:6],
                level=k + 1
            )
            area_list.append(area)

        Area.add_all(area_list)
        area_list = []


if __name__ == "__main__":
    main()
