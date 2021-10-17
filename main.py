# -*- coding: utf-8 -*-

from common.MongoConnect import MongoConnect

from pydantic import BaseModel, Field
from typing import Optional, List

from fastapi import FastAPI, Query, Path, Body
from faker import Faker
from enum import Enum
import random

app = FastAPI()


class Image(BaseModel):
    url: str
    name: str


class Person(BaseModel):
    name: str
    age: int
    address: str = None
    job: str = None


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(None, description='The description of the item', max_length=300)
    price: float = Field(..., gt=0, description='The price must greater than zero.')
    tax: Optional[List[float]] = None
    tags: List = []
    image: Optional[List[Image]] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "apple",
                "description": "one apple a day, docter leave me away",
                "tax": [1.3,32.2],
                "tags": ["fruit", "sweet"],
                "images": {
                    "name": "apple.jpg",
                    "url": "http://www.baidu.com/apple"
                }
            }
        }


class Address(Enum):
    America = "NewYork"
    China = "Beijing"
    Japan = "Tokyo"


@app.get("/")
async def index():
    return {"info": "welcome to my website."}


@app.get("/person/{person_name}")
async def get_person(person_name: str):
    """
    可以指定参数类型，系统会自动检测传入是否正确
    :param person_name:
    :return:
    """
    f = Faker()
    p_info = {
        "name": person_name,
        "address": f.address(),
        "age": random.randint(0, 100)
    }
    return p_info


@app.put("/user/{user_id}")
async def get_user(user_id: int = Path(..., title="The ID of the item to get", le=100, gt=30),
                   q: Optional[str] = None,
                   p: Optional[Person] = None):
    """

    :param user_id:
    :return:
    """
    user_info = {"user_id": user_id}

    if q:
        user_info.update({"q": q})

    if p:
        user_info.update({"p": p})
    # f = Faker()
    #
    # user_info = {
    #     "name": f.name(),
    #     "address": f.address(),
    #     "age": random.randint(0, 100),
    #     "id": user_id
    # }
    return user_info


@app.get("/address/{address_name}")
async def get_address(address_name: Address):
    return {"address": address_name, "city": address_name.value}


@app.get("/items/")
async def get_item(item_id: int, short: bool = None, limit: Optional[int] = None):
    item = {"item_id": item_id}

    if short:
        item.update({"doc": "welcom to use fastapi docs."})

    if limit:
        item.update({"limit": limit})

    return item


@app.post("/people/c")
async def insert_people(person: Person):
    """
    请求体测试
    :param person:
    :return:
    """
    p = {"name": person.name, "age": person.age, "address": person.address, "job": person.job}

    try:
        mongo_client = MongoConnect("person")
        mongo_client.insert(p)
        return {"ret_code": 200, "ret_info": "insert success"}

    except Exception as e:
        return {"ret_code": 500, "ret_info": f"insert failed: {e}"}


@app.get("/people/r")
async def read_people(p_name: Optional[str] = Query(..., max_length=10, min_length=5, regex="\w+")):
    """
    测试请求体，测试查询参数，字符串校验
    :param p_name:
    :return:
    """
    mongo_client = MongoConnect("person")

    try:
        if not p_name:
            data = mongo_client.read()
        else:
            data = mongo_client.read({"name": p_name})
        return {"data": data, "ret_code": 200, "ret_info": "success"}

    except Exception as e:
        return {"ret_code": 500, "ret_info": f"查询失败:{e}"}


@app.get("/people/test")
async def test_people(q: Optional[List[str]] = Query(
    None,
    title="People Test",
    min_length=3,
    description="Query string for the items to search in the database that have a good match")):

    query_item = {"q": q}
    return query_item


@app.get("/people/test2")
async def test_people2(q: list = Query(None)):
    query_item = {"q": q}
    return query_item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Optional[Item] = None,
                      person: Person = Body(..., example={
                        "name": "Denise Gonzalez",
                        "address": "146 Ramirez Rapids\nNew Brittanyville, NM 73748",
                        "age": 67,
                        "job": "Database administrator"
                        })):
    result = {
        "item_id": item_id,
        "person": person,
        "item": item
    }
    return result