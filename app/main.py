from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

from starlette.responses import Response

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


try:
    conn = psycopg2.connect(host='localhost', database='myfastAPIdatabase',
                            user='postgres', password='postgres', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('database connecion was successfull')
except Exception as error:
    print('connection failed ', error)


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_indexOf_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "favorite foods", "content": "I like pasta", "id": 2}]

# path operation i.e routes @decorators


@app.get("/")
async def root():
    return {"message": "welcome to my api"}


@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createpost(post: Post):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 100000)
    # my_posts.append(post_dict)
    # convert pydantic model to dict use .dict() func
    cursor.execute("""INSERT into posts (title, content,published) VALUES(%s,%s,%s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()  # push changes to the database

    return {"data": new_post}


# schema -> title str, content str

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # post = find_post(id)

    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'msg': f"post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {"single_post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting a post
    # index = find_indexOf_post(id)
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    # my_posts.pop(index)
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    # index = find_indexOf_post(id)
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    conn.commit()
    return {'message': updated_post}
