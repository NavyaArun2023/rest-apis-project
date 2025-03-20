import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
# from db import stores
from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

blp=Blueprint("stores",__name__,description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self, store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store
        # try:
        #     # You presumably would want to include the store's items here too
        #     # More on that when we look at databases
        #     return stores[store_id]
        # except KeyError:
        #     abort(404, message="Store not found.")


    def delete(self, store_id):
        store=StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return{"message":"Store deleted"},200
        # raise NotImplementedError("Deleting an store not implemented")
        # try:
        #     del stores[store_id]
        #     return {"message": "Store deleted."}
        # except KeyError:
        #     abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200,StoreSchema(many=True))
    def get(self):

        # stmt = select(StoreModel)
        # result = db.session.execute(stmt).scalars()
        # return list(result)
        return StoreModel.query.all()
        # raise NotImplementedError("listing stores is not implemented")
        # return {"stores": list(stores.values())}
        # return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self,store_data):
        # (((note:name can be of anything here i written store_data)))
        # store_data = request.get_json()
        # if "name" not in store_data:
        #     abort(
        #         400,
        #         message="Bad request. Ensure 'name' is included in the JSON payload.",
        #     )
        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message=f"Store already exists.")
        # store_id = uuid.uuid4().hex
        # store = {**store_data, "id": store_id}
        # stores[store_id] = store

        # return store,201
        store=StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400,message="store with that name already exists")
        except SQLAlchemyError:
            abort(500,message="An error occured while creating item")
        return store,201